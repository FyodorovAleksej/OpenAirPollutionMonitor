# YARN

features:
- multi-tenancy
- scalability
- compatibility

components:
- client
- resource manager (know resources in cluster)
  - scheduler (have several configurations)
- application master (located in every node. Task cycle, and container)
- node manager (every node. Manages resources on a node level)
- container

is as framework (abstraction), that used for spark, maprduce, tez and so on

App master - общается с resource manager и, работая с node manager, для монитроринга components tasks


### Schedulers:
1) FIFO (по очереди)
2) Capacity scheduler (полное разделение)
3) Fair scheduler (временное разделение)


### Security:
- Ranger
- Knox
  








  
# MapReduce

stages:
- input data
- map (many)
- shuffle & sort
- reduce (0, 1, or more)
- results

Map:
- process input blocks
- produce (key-value) pairs
- executed in parallel

Reduce:
- take (key-value) pairs sorted by keys
- combine/aggregate them to
- produce final result
- can be 0, 1 or more (executed in parallel)

Architecture:
- JobTracker (1 instance)
- TaskTracker (for each node)

map(key, value) => list(intermediateKey, intermidiateValue)

Mapper types:
1) Identity
2) Inverse
3) Regex
4) Token count

reduce(intermediateKey, intermediateValue) => list(outKey, outValue)

reducerTypes:
1) IdentityReducer
2) LongSumReducer


MapReduce is designed for batch processing








# HIVE

## Hive UDF

### UDF:
- User defined functions (UDF)
- User defined aggregate function (UDAF)
- User defined table function (UDTF)


### Usage:
1. implement UDF interface
2. adding jar to classpath
3. register function
4. using in query


### Incremental updates:
- Master table (internal)
- Delta table (external)
- Reconciliation (согласование) view
- Reporting table (snapshot of reconciliation view)

Cycle:
1. if doesn't exist:
  1. import data to HDFS
  2. create internal master table
2. if already exist:
  1. import updated data to HDFS
  2. create external Delta table (pointing location of the new data)
  3. create reconciliation view as a UNION from Master and Delta (смержить дельту и мастер)
  4. create internal Reporting table from reconciliation view (репорт - таблица)
  5. remove data from Delta by removing files from HDFS (удаление дельты)
  6. recreate Master (from Reporting table) (перемещение из репорта в мастер)

### Merge (from HIVE 2.2) - **only on transaction table (только для транзакционных таблиц)**

merge = update + insert + delete - **all only on transaction table**
(from HIVE 0.14)
### Upsert
Upsert = update + insert






## HIVE ACID
### Transaction tables:
requirements (требования к транзакционным таблицам):
- enabled globally (доступна локально)
- created with tblproperties("transactional"="true") - пропертя
- (not required, but strongly recommend) partitioning
- table is bucketed
- table is internal
- ORC file format

**you cannot change the transactional attribute after creating transactional table (table - transactional forever)** - таблица навсегда остаётся транзакционной

### creating transactional table example:

---

```sql
CREATE TABLE transactional_table (id int, username string)
PARTITIONED BY (timestamp_date date)
CLUSTERED BY (username) INTO 3 BUCKETS
STORED AS ORC TBLPROPERTIES ('transactional'='true')
```

---

### transactional tables properties:
- disabled by default (отключена по-умолчанию)
- full ACID semantics on the row level (полная ACID-семантика на уровне записей)
- auto-commit. No BEGIN, COMMIT, ROLLBACK. Only ABORT (manually or automatically (when heartbeat lost)) (автоматические коммиты. Только 'ABORT' - в-ручную или автоматически при потере сигнала (heartbeat))
- only SNAPSHOT level isolation is supported (поддерживается только 'SNAPSHOT' уровень изоляции)
- LOAD DATA is not supported (LOAD DATA не поддерживается)
- Required for UPDATE, DELETE, MERGE (Обязательна для операций 'UPDATE', 'DELETE', 'MERGE')
- Optimistic concurrency (оптимизированный конкурирующий доступ (через локи))
- Designed for updates in bulk (массированные updat-ы) (**can use HIVE streaming API for small batches**)
- Partitioning is recommended for large datasets (partitioning - рекомендуется для больших датасетов)
- Periodically compacted (несколько дельт объеденяется в 1, если они маленькие) (**each transaction create delta file. If delta files was small - compacting and merge in one delta file**)

### High level components:
- Base files - containing of data
- Delta files - (0 or more) (for each update and delete)
- Compactor - merges Delta and Base files for each bucket. (**background mapreduce job. For each bucket separately. Base and delta files are created per bucket. You can set - how often compactor can run, or max count of background jobs of compactor**) (мержит base и delta файлы в каждом бакете)
  - major compaction - takes delta files and merge with base files.
  - minor compaction - many small files to big. (объединяет маленькие дельты в большую)
- Transaction/Lock manager - manages transaction locks in HIVE Metastore. **durable and restored if cause of server failure**


transaction initiator and lock holders - отсылают heratbeat
**transaction initiators and lock holders periodically send heartbeats to the Metastore. It's need to remove any abounded transactions and logs**

**Update and delete - doesn't modify the existing table files, they create new delta files** (они создают новые дельты)

### New commands
![ACID_commands](./img/HIVE/HIVE_ACID_newCommands.PNG)

| Command                  | Description                                                                             | **Notes**                                                                                                                                                                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```SHOW TRANSACTIONS```  | list of all currently open and aborted transactions                                     | **show id, state, author, machine, timestamp of start, last heartbeat time**                                                                                                                                                     |
| ```ABORT TRANSACTIONS``` | cleans up the cpecified transaction IDs from the Metastore                              | **except 1 or more IDs avoiding the transaction, what kill the related query immediately. Instead ACID queries periodically heartbeat and if detect, that underline transaction has been aborted - that will exit at that time** |
| ```SHOW LOCKS```         | displays the locks on a table or partition                                              | **transaction identifier. Locks can be: shared, read/write or exclusive**                                                                                                                                                        |
| ```SHOW COMPACTIONS```   | list of all tables and partitions currently being compacted or scheduled for compaction | **type of compaction, database, table, state, start time, duration and other properties**                                                                                                                                        |







## HIVE STREAMING
### Intro

for supporting continuous data ingestion (кормление) (many records -> many small delta files -> highly inefficient -> overload hdfs namenode (additional metadata)) *namenode stored metadata in memory*

committed in small batches of records into in existing HIVE partition or table. (*the support of dynamic partitioning has been only added since HIVE 3.0*)
after committing - it becomes immediately visible for all HIVE queries, initiated subsequently

Only the transactional tables are supported

- by default only delimited (csv, strict json, regex) data is supported. Can be extended (*Hive provides record writer interface*)
-


### usage:
- write custom application, to connect to HIVE and run streaming API methods on that connection
- when connection will be returned from hive -> application generally entered a loop (fetchTransactionBatch) on that connection and write a series of transactions
![HIVE_STREAMING_loop](./img/HIVE/HIVE_STREAMING_fetchTransactionBatchLoop.PNG)
  - *transaction doesn't includes data from more than 1 partition*

It loop implemented by yourself, or using existed variant (NiFi, Flume, Storm)

### streaming updates:

In HIVE 2.0:
- adding "Streaming Mutation API" (deprecated in HIVE 3.0)
  - doesn't replace HIVE streaming API (**support merge type processes (writing and deletes)**)
  - based on very different transaction model
  - designed to frequently apply large sets of mutations to a dataset in atomic fashion (**Ether all or none of the mutations are be applied. This instead mandate using of a single long-lived transactions**)
  - for applying mutation to a record one must have some unic key, that identify record (primary keys are not a constantly construct provide by HIVE. Internally HIVE uses record identifiers, stored in virtual store id column)
  - any process that wishes to issue mutations to a table, with this API, must have available the cores writing ROW__IDs for the target records (read current snapshot of data -> join the mutation on some domain specific primary key for obtain core ROW__ID)
  - provide record writer and modifier

In HIVE 3.0:
- streaming API was simplified (auto-rollover of the batches, automatic heart beating (provide heartbeat method (called after creating batch)), writers accept an input stream instead of a byte array)
  - contain heartbeat thread, that automatically send heartbeat to all open transactions
- supporting dynamic partitions (**a record writer, running in dynamic partitioning mode except the partition column was last column in each record**)
- in progress (avro, multi file and others)





## HIVE explain

EXPLAIN - show plan of the query execution

example:
![HIVE_EXPLAIN_planExample](./img/HIVE/HIVE_EXPLAIN_planExample.PNG)

modifiers:
- ```EXTENDED```  - additional information about operators in a plan (physical information)
- ```DEPENDENCY``` - additional information about inputs in the plan (shows attributes for the inputs) (inputs contain tables and partitions(**table is present even if none of the partition is excess in a query**)), show parents

3 parts:
- abstract syntax tree of the query
- dependencies between different stages of the graph
  - additional information about
- description of each of the stages
  - show sequence of operators with the method data, associated with operators (expression for the operator)


### HIVE statistics

 query optimization

statistics - one of the inputs in optimization
scope:

  1. Milestone - to support table and partition levels statistics. - stored in a HIVE Metastore (supporting for partitions)
    - number of rows
    - number of files
    - size in bytes
    - (for tables : numbers of partitions)
  2. Milestone support column level statistics:
    - top keys (name and top key values stored in partition or none partitions table suit information(if user doesn't use partitioning))
    (disabled by default)

- for new tables or partitions - statistic automatically used (by default) - stored in HIVE Metadate
- for existing - can use ```ANALYZE``` command



## HIVE schema optimization

- normalization - create several relational tables, that can be combined at the runtime, to get result. (*joins are expensive and difficult operations to perform*)
  - cost and benefit balance of normalization is different between RDBMS world and HIVE
  - the use cases for HIVE are not transactional, they are analytic.
  - many way joins required for normalized data tend to be more expensive for HIVE
  - HIVE's massive parallelism eliminates many of the disk I/O limitations of an RDBMS
  - HIVE is also often used with data volumes for which it would impractical to use normalized data
  - The savings in data volume (that would be result of the normalization on RDBMS) are often more than offset by the high compression rates achievable with a large data blocks in HIVE
*abounded CPU and absence of central processing bottleneck makes compression and decompression relatively cheap*
**while a fully normalized schema can be often be defined for HIVE data, it's common practice to relax many aspects of normalization and infect HIVE also explicitly support some kinds of none normalized data storage like storing accessing lists and maps within a column**

### HIVE integration
| name                      | description                                                                                              | API                                                                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Hive Accumulo integration | Apache Accumulo - sorted distributed key value store, based on a Google Big Table Paper                  | API methods are in terms of keys and values, which present the highest level of flexibility in reading and writing data              |
| Hive HBase integration    | HBase - Hadoop database. Distributed scalable bigdata store                                              | Allows hive query language statements to access HBase tables for both read (SELECT) and write (INSERT). Can be used JOINS and UNIONS |
| Druid integration         | Druid - opensource analytics datastore, designed for business intelligence or lab queries on events data | provide real-time low level data ingestion, flexible data exploration and fast data aggregation                                      |


DRUID

### Hive setting

- engine selected globally, but can be changed per in each individual query through HIVE session variables

TEZ optimizations:
- allow using containers for success of phases of processing
- provide 3-wormed containers, so that jobs can start instantly

ORC file format (Optimized Row Column Format)
- column oriented and enables mummeries HIVE optimizations and including impression for individual column data types:
  - skipping processing, entire chunks of files if they are not relevant to a query
  - skipping decompression of columns, that are not reliving to a query projection
  - provides parallelism
- support ACID transaction (supports only in ORC format)
- **Predicate push-down in ORC**
  - ORC reader uses the information in the index to enable a family of optimizations, called "push-down predicates" (HIVE passes the "WHERE" conditions for a query down to the reader, which can use for predicate to determine - which records are relevant to the query before bothering to unpack the columns. If the value form the WHERE condition is not within minimum/maximum range - that entire chunk of file can be skipped)
- **Vectorized processing in ORC**
  - low-level optimization (CPU uses (process many rows at the time))
  - can be enabled globally, or per query (HIVE configuration properties)
- **Cost based optimizer (CBO) in ORC**
  - tune up the query plan, according to Metadata, it has been gathering in advance from the data. (Include:
      - minimum
      - maximum
      - number of distinct values
      - partitions
      - table DDL
      - and so on)
  - can be off by the configuration properties
-  **Partition and bucket prunning**
  - by default - stored in a single logical HDFS direct way. HDFS has 2 ways to break up the data structure to facilitate query and data management:
    - partitioning. Reader doesn't have to traverse any brunch of a HDFS directory tree, that is qualified by one of the predicates in a query WHERE close.
    - bucketing. Pursed a values into a fix numbers of files inhor for delete distribute to load
  - after HIVE 2.0 support bucket prunning, when used TEZ engine. Speeds up where conditions and based on parameter value allows to read the relevant bucket file, rather then all files in buckets, that belong to a table










# KAFKA

## Kafka architecture

### Kafka overview
Kafka - is a distributed streaming platform, which has 3 key capabilities:
- publishing subscribe to streams of records similar to a message queue or enterprise messaging system
- store streams of records in a fault-tolerant durable way
- process streams of records as they occur

kafka used for 2 broad classes of applications:
1. building real-time streaming data pipelines, that reliably gets data between systems or applications
2. building real-time streaming applications, that transform or react to the streams of data

### Publish/subscribe pattern
![KAFKA_ARCHITECTURE_architecture](./img/KAFKA/KAFKA_ARCHITECTURE_architecture.PNG)

Properties of Kafka:
- is a fast, scalable, durable, and fault-tolerant publish-subscribe messaging system
- is often used in place of traditional message brokers like JMS and AMQP because of its higher throughput, reliability and replication
- may work in combination with Storm, Spark, Samza, Flink, etc. For real-time analysis and rendering of streaming data
- Kafka brokers massive message streams for low-latency analysis in Enterprise Apache Hadoop

### Typical use cases:
- messaging. Because:
  - better throughput
  - built-in partitioning
  - replication
  - fault-tolerance
- streaming processing. After Kafka 0.10 -> light-weight Kafka Streaming
- metrics collection and monitoring
- website activity tracking
- event sourcing (CDC)
- log aggregation
- commit log (log replication)

### Kafka key qualities:
- Scalability - distributer messaging system scales easily with no downtime
- Durability - persists messages on disk, and  provides intra-cluster replication
- Reliability - replicates data, supports multiple consumers, and automatically balances consumers in case of failure
- Performance - high throughput for both publishing and subscribing, with disk structures that provide constant performance even with many terabytes of stored messages

### Kafka APIs:
1. The **Producer API**
  - publishing stream of records
2. The **Consumer API**
  - subscribing to topics and processing the stream of records
3. The **Connect API**
  - building and running reusable producers or consumers
4. The **Streams APIs**
  - application as a stream processor, consuming an input stream from topics and producing an output topics



## Kafka Topics, partitions and replicas

### Kafka topics
For each topic the Kafka cluster maintains the structure commit log with 1 or more partitions. Kafka appends new messages to the partition in an order immutable sequence. Each message in a topic is assigned as a sequential number, that uniquely identifies the message within a partition. The number is called as "offset" and it's represented in a diagram by numbers within each cell

| Name        | Offsets                      |
| ----------- | ---------------------------- |
| partition 0 | 0,1,2,3,4,5,6,7,8,9,10,11,12 |

### Kafka partitions
partitions support for topics provides parallelism in addition.

- Topic consists of 1 or more partitions
- Each partition is ordered, immutable sequence of messages that is continually appended to a commit log

### Kafka replicas
replica - backup of the partition
replicas - never used for read or write data. They are used to prevent data lost.

Within a cluster of brokers - 1 broker will also function as a cluster controller, elected automatically from the live members of the cluster.

The controller responsible for administrative operations, including assigning partitions to brokers and monitoring for broker failures.

A partition is owned by a single broker in a cluster. That broker is called **"Leader" of the partition**

### Kafka replication
2 types of replicas:
1. Leader replica - each partition has a single replica, designated as the **Leader**. All produce and consume requests go through the leader in order to guarantee consistency
2. Follower replica - all others in a partition -> **Followers**. Don't serve client requests. They only job - replicate messages from the leader and stay up to date with the most recent messages, that the leader has. On a leader crushes - 1 of the follower replica will be promoted to become a new leader for the partition

### In-sync replicas
**replica - In-sync, if it:**
- has an active session with Zookeeper. (it sent a heartbeat to Zookeeper in the last 6 seconds (configurable))
- fetched messages from the leader in the last 10 seconds (configurable)
- fetched the most recent messages from the leader in the last 10 seconds

If requirement doesn't following - replica is **Out-sync**
it isn't enough the followers still getting messages from the leader. It must have **almost known leg**
If Out-sync replica connect to Zookeeper again and fetch most recent messages -> this become In-sync again


can be Out-sync with the leader in following reasons:
1. slow replica (follower replica not able to catch up with the rights of the leader of the settled period of time (input-output bottleneck))
2. stack replica (follower replica, that stopped fetching of the leader for the settled period of time (when replica reduced by garbage collector pose or it failed or died))
3. bootstrapping replica (when user increases the replication factor of the topic, the new follower replicas are Out of sync, until they fully copied up to the leader log)

A replica is consider to be Out of sync or legging when it falls sufficiently behind the leader of the partition

In Kafka 0.8.2 a replica's leg is measured either intern of number of messages it is behind the leader or the time for witch the replica has not attempted to fetch new data from the leader.
The former is used to detect slow replicas while the letter is used to detect halted or dead replicas

one configured to rule them all.
Offer realize that there is only one thing, that really matters another to detect either stack or a slow replica. And that's a time, which replica has been out of sync with the leader
removing the leg definition in terms of number of messages gets read to the need to gas the right value based on the expected traffic for the topic

### Producer load balance
Producers publish data to the topics of their choice. The producer is responsible for choosing which message to assign to which partition within the topic.
This can be done in round-row been a fashion simply to balance load or it can be done according to some semantic partition function

### Consumer load balance

messaging have 2 models:
- querying - pool of consumers may read from a server and each message goes to one of them
- publish subscribe - the message is broadcast to all consumers

Kafka - the single consumer abstraction, that generalizes both of them = **The consumer group** - Consumers labels themselves with a consumer group name, and each message published to a topic, is delivered to 1 consumer instance within each subscribe consumer group
If all consumers have same consumer group -











# Spark

## Shared variables:
1) broadcast variables
- use torent like protocol
- read-only
- similar to MapReduce distributed cache
- to implement map side-joins
- not shipping a copy with the given task

2) accumulators
- write-only
- used for calculate statistics (counters and summs)
- for display at spark web ui - must be named
- extend AccumulatorParam for custom type

## Cashing Dataframe

- cashing at interval
- used for restoring result after failure
- effective if there is main dataframe, around which we perform operations

usage:
- sqlContext.cacheTable("...")
- dataFrame.cache()

## Smart sources
- DataSource API
- server side filtering
- column prunning
- partition prunning

Examples:
- Parquet, ORC
- Cassandr, RDBMS, Hbase

## JDBC
- spark can read from another databases by using JDBC
- results returned as DataFrame
- smart sources capabilities

## Catalyst
- build a tree of operations based on a received queries
- based on a functional progamming (on Scala)

process:
- validate query
- there are columns from query?
- build syntax tree, based on rules

Execution plan:
planing:
- parse logical plan (afer parsing DSL (from HIVE QL parser, DSL parser and so on))
- analyse logical plan
- optimize logical plan
- physical plan or spark plan

parts of query:
- expressions 
- attribute (column)

## Cost-based optimizer (Spark 2.3)

getting statistics

- table statistics:

```sql ANALYZE TABLE table-name COMPUTE STATISTICS```

- column statistics:

```sql ANALYZE TABLE  table-name COMPUTE STATISTICS FOR COLUMNS column-name1, name2, ...```

optimized by this statistic

## Tungsten
initiatives:
- Memory management and Binary Processing
- Cache-aware computation
- Code generation

manage memory more efficient, than JVM (builds on sun.misc.Unsafe (C-style memory access))

cache aware computation
more efficient usageof L1/L2/L3 CPU caches

code generation **FIX** this issues:
- virtual function calls
- Branches based on epression type
- Object creation due to primitive boxing
- Memory consumption by boxed primitive objects


## JOINS

join types:
1) sort-merge join (default)
  - for false: ```spark.sql.join.preferSortMergeJoin = false```
  - *keys must be sortable*
2) Shuffle hash join
  - when keys are not sortable or keys disabled
  - can build local hashmap for partition
3) broadcast join (map-side join)
  - for using:
    - set max size: ```spark.sql.join.autoBroadcastJoinTreshold = 10485760```
    - or ```org.apache.sql.functions: def broadcast[T] (df: Dataset[T])```
  - it don't use shuffle at all
  - can build local map for table

## Tuning techincs

(spark context text file)

Components:
- Driver (1)
- Cluster manager (1 (Mesos, Yarn, Spark, sql))
  - Executors (on nodes)
    - has cache
    - tasks
  - Shuffle service

Setting driver memory:
```$ spark-shell -driver-memory 8g```
Setting executor memory:
```$ spark-shell -executor-memory 8g```

Scaling driver:

dynamic allocation of the resources:

```ini
spark.dynamicAllocation.enable=true
spark.dynamicAllocation.executorIdleTimeout=2m
spark.dynamicAllocation.minExecutors=1 (spark automatically reduce to 0)
spark.dynamicAllocation.maxExecutors=2000
spark.shuffle.service.enabled=true
```

### Spark memory:
- execution memory (used for computations in shuffles, joins, sorts and aggregations)
- storage memory (for caching)
  
- User memory (for own datastructures)
- Reserved memory (for internal needs)

#### executor memory off-heap:
- objects is serialized to byte array
- managed by the operating system but stored outside the process heap in native memory
- not processed by garbage collector
- slower than on-heap storage, but faster, than read/write from the disk

for turn on:
```ini
spark.memory.offHeap.enabled=true
spark.memory.offHeap.size=3g
```
  

#### speculation
if 1 task run very slow:
```ini
spark.speculation=true
spark.speculation.interval=100

spark.speculation.multiplier=1.5
spark.speculation.quantile=0.95
```

#### level of parallelism
(depends on number of partitons)
```ini
spark.sql.shuffle.partition=200
spark.default.parallelism=10
```


### Debug and testing
usage in local mode (standalone)

- debug by IDE
- logging
- with sample dataset


Unit testing:

- creating spark context with master = local
- run operations
- run sparkContext.stop()
- make sure, that you not in the 'finally' block or in the 'tearDown' method
  
or trying spark-testing-base framework  


YARN client mode: debugging:
- spark application launched by IDE
- Driver run on the developer's machine
- executors will be scheduled and launched on cluster

**developer machine and application master's node in the cluster have to be able to reach each other**


  












# DATA MOVEMENT
## NIFI Intro

### Problem statement

Common:

1. The problem to bring data from producers to consumers.
  - Producer: anything(application servers, database servers, manufacturing machines, smart home appliances and personal wearables, cars and so on).
  - Consumers: represented by alive people, another machines including storage only as well as AI enabled services

2. Different standards

#### Problems:

- Formats
- Protocols
- Compliances
- Schemas
- Volume/Variety/Velocity of data
- Ensuring security
- Ensuring reliability
- Ensuring availability
- Additional effort to onboard new producer/consumer


The client was in the process of migration to microservice architecture and every service exposed data in their own way: some of them exposed data in realtime manner while another provided only batch interface

Disparate transport mechanism which can transport, route, transform information, takes care about reliability and availability.


#### NIFI Overview:

A comprehensive and readily consumed form is found in the Enterprise Integration Patterns

- Framework to build scalable direct graphs of data routing, transformation and system mediation logic
- Originally was developed by NSA and then Open sourced
- Apache top-level project, actively supported by Hortonworks
- Hortonworks Data Flow is based around Apache NIFI

#### NIFI Features:

- Web-based user interface
- Highly configurable:
  - Loss tolerant vs guaranteed delivery
  - Low latency vs high throughput
  - Dynamic prioritization
  - Flow can be modified at runtime
  - Out of box back pressure mechanism
- Data provenance
  - Build your own processor and more
  - Enable rapid development and effective testing
- Security (SSL, encrypted content, authentication and authorization)

**Flow Based Programming** - is a programming paradigm that defines applications as networks of "black box" processes, which exchange data across predefined connections by message passing, where the connections are specified externally to the processes.
These black box processes can be reconnected endlessly to form different applications without having to be changed internally.
**FBP is thus naturally component-oriented**.

| FBP term           | NiFi term           | Definition                                                                                                                  |
| ------------------ | ------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Information packet | FlowFile            | Each object moving through the system                                                                                       |
| Black Box          | Flow File processor | Performs a work, doing data routing, transformation or mediation between systems                                            |
| Bounded buffer     | Connection          | The linkage between processors, acting as persistence queues and allowing various processed to interact in a different rate |
| Scheduler          | Flow Controller     | Maintains the knowledge how processes are connected and manage resources                                                    |
| Subnet             | Process Group       | A set of processes and their connections which can receive and send data via ports                                          |


**FlowFile** - is an object transported through the system
**NiFi** - is data agnostic which means FlowFile can contain any type of information in any format

*Similar to HTTP data, Flow file contains 2 parts:*
  - **Header, with metadata**
  - **Body, with message content**


### NiFi architecture:

NiFi executes within a JVM on a host operating system. The primary components of NiFi on the JVM are as follows:
- **Web Server** - The purpose of the web server is to host NiFi’s HTTP-based command and control API.
- **Flow Controller** - The flow controller is the brains of the operation. It provides threads for extensions to run on, and manages the schedule of when extensions receive resources to execute.
  - **Extensions** - There are various types of NiFi extensions which are described in other documents. The key point here is that extensions operate and execute within the JVM.
- **FlowFile Repository** - The FlowFile Repository is where NiFi keeps track of the state of what it knows about a given FlowFile that is presently active in the flow. The implementation of the repository is pluggable. The default approach is a persistent Write-Ahead Log located on a specified disk partition.
- **Content Repository** -  The Content Repository is where the actual content bytes of a given FlowFile live. The implementation of the repository is pluggable. The default approach is a fairly simple mechanism, which stores blocks of data in the file system. More than one file system storage location can be specified so as to get different physical partitions engaged to reduce contention on any single volume.
- **Provenance** - RepositoryThe Provenance Repository is where all provenance event data is stored. The repository construct is pluggable with the default implementation being to use one or more physical disk volumes. Within each location event data is indexed and searchable.

*NiFi is also often operated within a cluster.*

**Apache Nifi can operate on a single machine as well as in a cluster to increase reliability, availability and throughput of solution.**
 *Starting with the NiFi 1.0 release, a Zero-Master Clustering paradigm is employed*


 *Each node in a NiFi cluster performs the same tasks on the data, but each operates on a different set of data*

 *Apache ZooKeeper elects a single node* **as the Cluster Coordinator** *, and failover is handled automatically by ZooKeeper.
  All cluster nodes report heartbeat and status information to* **the Cluster Coordinator.**
  *The Cluster Coordinator is responsible for disconnecting and connecting nodes.*
  **Additionally, every cluster has one Primary Node, also elected by ZooKeeper.**

  As a DataFlow manager, you can interact with the NiFi cluster through the user interface (UI) of any node. Any change you make is replicated to all nodes in the cluster, allowing for multiple entry points

### NiFi Example:

![example](./img/DATA_FLOW/NiFi_Example.PNG)

1. Stats about processors,
  - how many records (volume of data) received as an input,
  - how many were sent out in the last 5 min,
  - etc
2. This is a queue between processors (connection),
  - it’s possible to see the amount of data queued between processors and that’s how NiFi implements black pressure
3. Processor just need to be drag and drop, then configured. *Exclamation mark is a sign that not all required attributes are set and processor requires additional configuration before starting flow*
4. *For every processor we can set up failure route, which define behavior in the case when FlowFile can’t be handled by a processor.* (**It allows to implement dead letter queue**)

#### NiFi extending:

Apache NiFi functionality can easy be extended by custom processors
In order to do that, follow official documentation to extend NiFi class and override required methods with custom business logic (for instance, resolving geo coordinates to closest human readable address):

- Pack your code into **NAR (jar for NiFi)**
- Add your NAR to NiFi classpath
- Add your own processor to flow as needed


#### MiNiFI Overview:
MiNiFi unlocks possibility to collect and preprocess data on source side (edge computation) and deliver data to data processing cluster, all in reliable way.

MiNiFi is implemented in Java (less then 40MB distribution) and C++ (about 700KB distribution and required 1MB RAM to run, targets IoT devices)



## NIFI Deep Dive

Components:
### 1. FlowFile repository:

Features:
- Write-Ahead Log of the metadata of each FlowFile which currently exists in the system
- FlowFile repository protects against hardware and system failures by keeping a record of what was happening on each node at that time 

FlowFiles that are actively being processed by the system are **held in a hash map in the JVM memory**

This makes it very efficient to process them, **but requires a secondary mechanism to provide durability of data across process restarts due to a number of reasons**, such as power loss, kernel panics, system upgrades, and maintenance cycles
This FlowFile metadata includes:
- all the attributes associated with the FlowFile
- a pointer to the actual content of the FlowFile (which exists in the Content Repo)
- the state of the FlowFile, such as which Connection/Queue the FlowFile belongs in.

*This Write-Ahead Log provides NiFi the resiliency it needs to handle restarts and unexpected system failures*

### 2. Content repository:

Features:
- A place in local storage where the content of all FlowFiles exists
- This repository **utilizes the immutability and copy-on-write paradigms to maximize speed and thread-safety as well**


The core design decision influencing the Content Repo is **to hold the FlowFile’s content on disk and only read it into JVM memory when it’s needed.**

*This allows NiFi to handle tiny and massive sized objects without requiring producer and consumer processors to hold the full objects in memory.*

As a result, actions like:
- splitting
- aggregating
- transforming very large objects

**: are quite easy to do without harming memory**

the reference to FlowFile's content can simply be referred to as a **"pointer"** to the content
Though, the underlying implementation of the FlowFile Content reference **has multiple layers of complexity**
**The Content Repository is made up of a collection of files on disk.**
**Like GC process, there exists a dedicated thread in NiFi to analyze the Content repo for un-used content**


### 3. Provenance repository:

Features:
- Where the history of each FlowFile is stored and used to build data lineage
- Each time that an event occurs for a FlowFile - **a new provenance event is stored**
- Such level of details allows to replay flow from specific point in time if data still available in the other repos

This history is used to provide **the Data Lineage (also known as the Chain of Custody)** of each piece of data
Each time that an event occurs for a FlowFile:

- FlowFile is created
- forked
- cloned
- modified
- etc.

**: a new provenance event is created.**

**This provenance event - is a snapshot of the FlowFile** as it looked and fit in the flow that existed at that point in time


When a provenance event is created, **it copies all the FlowFile’s attributes and the pointer to the FlowFile’s content and aggregates that with the FlowFile’s state (such as its relationship with other provenance events) to one location in the Provenance Repo.**
**This snapshot will not change, with the exception of the data being expired.** The Provenance Repository holds all of these provenance events for a period of time after completion, as specified in the 'nifi.properties' file.

A common use-case for this is when a particular down-stream system claims to have not received the data. The data lineage can show exactly when the data was delivered to the downstream system, what the data looked like, the filename, and the URL that the data was sent to – or can confirm that the data was indeed never sent. In either case, the Send event can be replayed with the click of a button (or by accessing the appropriate HTTP API endpoint) in order to resend the data only to that particular downstream system. Alternatively, if the data was not handled properly (perhaps some data manipulation should have occurred first), the flow can be fixed and then the data can be replayed into the new flow, in order to process the data properly.

*Keep in mind, though, that since Provenance is not copying the content in the Content Repo, and just copying the FlowFile’s pointer to the content, the content could be deleted before the provenance event that references it is deleted.
This would mean that the user would no longer able to see the content or replay the FlowFile later on.
 However, users are still able to view the FlowFile’s lineage and understand what happened to the data.*

### 4. Flow Controller:

Features:

- The Flow Controller maintains the knowledge of how processes connect and manages the threads and allocations thereof which all processes use.
- The Flow Controller acts as the broker facilitating the exchange of FlowFiles between processors.

*When you open and build flow in NiFi UI, this flow is actually constructed and then executed by flow controller which spin up several auxiliary services to run processors itself*

### 5. Web Server:

Features:
- UI interface to access and manage NiFi flows
- Access can be protected by different means to ensure only authorized  access is possible (via Kerberos, ldap, etc)
- Users can be configured with different roles

### FlowFiles flowing in cluster:

*turn to sync on disk, otherwise FlowFiles are cached in memory and can be lost*


### EPAM Using:
2 technology competency at Epam grew up around NiFi:
- Big Data Competency Center
- Integration Competency Center

---













# WORKFLOW

## Oozie

### Oozie Intro
**Oozie - is an extensible, scalable and reliable system to define, manage, schedule, and execute complex Hadoop workloads via web services.**
 More specifically, this includes:

 - XML-based declarative framework to specify a job or a complex workflow of dependent jobs
 - Support different types of actions such as Hadoop Map-Reduce, Spark, Pipe, Streaming, Pig, Hive and custom java applications
 - Workflow scheduling based on frequency and/or data availability
 - Monitoring capability, automatic retry and failure handing of jobs
 - Extensible and pluggable architecture to allow arbitrary grid programming paradigms
 - Authentication, authorization, and capacity-aware load throttling to allow multi-tenant software as a service

### Oozie:

 - **Oozie is a server based Workflow Engine** specialized in running workflow jobs with actions that run different kind of Hadoop jobs.
 - **Oozie is a Java Web-Application** that runs in a Java servlet-container.
 - For the purposes of Oozie, a workflow is a collection of actions **arranged in a control dependency DAG (Directed Acyclic Graph)**.
   **"control dependency" from one action to another** means that **the second action can't run until the first action has completed.**
 - Oozie workflows definitions are **written in hPDL** (a XML Process Definition Language similar to JBOSS JBPM jPDL).
 - Oozie workflow actions **start jobs in remote systems** (i.e. Hadoop MR, Spark).
  Upon action completion, the remote systems callback Oozie to notify the action completion, at this point Oozie proceeds to the next action in the workflow.
 - Oozie workflows contain control flow nodes and action nodes:
   - Control flow nodes **define the beginning and the end of a workflow** (start, end and fail nodes) and **provide a mechanism to control the workflow execution path** (decision, fork and join nodes).
   - *Action nodes are the mechanism by which a workflow triggers the execution of a computation/processing task.*
 - Oozie workflows **can be parameterized** (using variables like "${inputDir}" within the workflow definition).


### Oozie architecture:
![oozie_architecture](./img/WORKFLOW/Oozie_Architecure.PNG)

An Oozie Server is deployed as **Java Web Application hosted in a Tomcat server**, and all of the **stageful information such as workflow definitions, jobs,  etc, are stored in a database**.
 *This database can be either Apache Derby, HSQL, Oracle, MySQL, or PostgreSQL.*

*There is an Oozie Client, which is the client that submits work, either via a CLI, and API, or a web service / REST.*


### Oozie high availability:
![oozie_high_availability](./img/WORKFLOW/Oozie_Architecture_High_Availability.PNG)

It is also possible to **deploy Oozie in a High Availability configuration**.
In production environments where the goal of removing single points of failure is important, it is critical that the element that schedules your Hadoop jobs doesn’t fall down.
**Oozie enables high availability by enabling multiple instance of Oozie Servers to all point to the same database.**

For this to work, **the database must be able to handle multiple concurrent connections**:
- PostgreSQL
- MySQL
- Oracle.

 **To achieve true HA, you should also have a redundant Database, synchronized with the principal database to remove the database as a SPOF.**

### Oozie components:
![oozie_components](./img/WORKFLOW/Oozie_Components.PNG)

**There are two basic types of Oozie jobs:**
1. Oozie Workflow jobs are Directed Acyclical Graphs (DAGs), specifying a sequence of actions to execute.
2. Oozie Coordinator jobs are recurrent Oozie Workflow jobs that are triggered by time (frequency) and data availability.

**Oozie Bundle** - provides a way to package multiple coordinator and workflow jobs and to manage the lifecycle of those jobs.

### Oozie example:

#### example *WORKFLOW*:

---

```xml
<workflow-app name="example" xmlns="uri:oozie:workflow:0.5">
  <global>
    <configuration>
      <property>
        <name>oozie.launcher.mapred.job.queue.name</name>
        <value>${queue}</value>
      </property>
    </configuration>
  </global>

  <start to="first-action" />

  <action name="first-action">
    <spark xmlns="uri:oozie:spark-action:0.1">
      <job-tracker>${jobTracker}</job-tracker>
      <name-node>${nameNode}</name-node>
      <master>yarn-client</master>
      <name>example</name>
      <class>com.epam.ProjectMainClass</class>
      <jar>${nameNode}${jobDir}/lib/example-0.1.jar</jar>
      <spark-opts>
        --queue ${queue}
      </spark-opts>
      <arg>${nameNode}${dataDir}</arg>
      <arg>${datePartition}</arg>
      <arg>${nameNode}${saveDir}</arg>
    </spark>

    <ok to="second-action" />
    <error to="fail" />
  </action>

  <action name="second-action">
	...
    <ok to="end" />
    <error to="fail" />
  </action>

  <kill name="fail">
    <message>Job failed [${wf:errorMessage(wf:lastErrorNode())}]</message>
  </kill>

  <end name="end" />

</workflow-app>
```

---

- In global block we set the queue for MapReduce task which will find the task and run it.
  - Parameters in curly brackets (e.g. ${queue}), we will declare in start command.
- In action block we describe Spark task and what should we do in case of ОК or ERROR status.
  - In spark block we describe environment, task definition and arguments.
    - Task running configuration describes in block spark-opts.

- If the task ends with ERROR status, execution proceeds to kill block and we show error message.


#### example *COORDINATOR*:

---

```xml
<coordinator-app name="example- coordinator" frequency="${frequency}" start="${startTime}" end="${endTime}" timezone="UTC" xmlns="uri:oozie:coordinator:0.1">
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
            <configuration>
                <property>
                    <name>datePartition</name>
                 	<value>${coord:formatTime(coord:dateOffset(coord:nominalTime(), -1, 'DAY'), yyyy/MM/dd")}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

---

- Here we define frequency of task execution, start and end time parameters.
  - The workflow block specifies the path to the directory where the workflow.xml file located.
    - The configuration block defines the value of the ‘datePartition’ property. It is the current date minus 1 day in the format yyyy/MM/dd.


#### example Job running (*COORDINATOR PROPERTIES*):

---

```conf
# environment
nameNode=hdfs://hadoop
jobTracker=hadoop.host.ru:8032

# path to the dir with coordinator.xml
oozie.coord.application.path=/example/jobs/example-job

# frequency in minutes (every 24 hours)
frequency=1440
startTime=2017-09-01T07:00Z
endTime=2018-09-01T07:00Z

# path to the dir with workflow.xml
workflowPath=/example/jobs/example-job

# user name to execute the task
mapreduce.job.user.name=username
user.name=username

dataDir=/example/data
saveDir=/example/status
jobDir=/example/jobs/example-job

queue=PROJECTS

# use libs from hdfs path instead of system libs
oozie.libpath=/example/jobs/example-job/sharelib
oozie.use.system.libpath=false
```

---

#### example commands:

| Describe                              | command                                                                                |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| Start the job with defined properties | ```oozie job -oozie http://hadoop.host.ru:11000/oozie -config coord.properties –run``` |
| Job status info                       | ```oozie job -info {job_id}```                                                         |
| Kill the job                          | ```oozie job -kill {job_id}```                                                         |
| Show jobs for user                    | ```oozie jobs -jobtype coordinator -filter user={user_name}```                         |


## Apache AirFlow

### AirFlow overview:

**Airflow - is a platform to programmatically author, schedule and monitor workflows.**
Use airflow to author workflows **as directed acyclic graphs (DAGs) of tasks**.
*When workflows are defined as code (Python), they become more maintainable, versionable, testable, and collaborative.*

The airflow scheduler executes your **tasks on an array of workers** while following the specified dependencies.
Rich command line utilities make **performing complex surgeries on DAGs a snap**.
*The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed.*

#### Principles:
- **Dynamic** - Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation.
*This allows for writing code that instantiates pipelines dynamically.*
- **Extensible** - Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant** - Airflow pipelines are lean and explicit.
*Parameterizing your scripts is built into the core of Airflow using the powerful Jinja templating engine.*
- **Scalable** - Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers.
*Airflow is ready to scale to infinity.*

### Airflow Architecture:

1. **Web Server**:
A daemon which accepts HTTP requests and allows you to interact with Airflow via a Python Flask Web Application. It provides the ability to pause, unpause DAGs, manually trigger DAGs, view running DAGs, restart failed DAGs and much more.

2. **Scheduler**:
A daemon which periodically polls to determine if any registered DAG and/or Task Instances needs to triggered based off its schedule.

3. **Executors / Workers**:
A daemon that handles starting up and managing 1 to many CeleryD processes to execute the desired tasks of a particular DAG.


### Airflow. Single node setup:
![one_node_image](./img/WORKFLOW/Airflow_One_Node_Setup.PNG)

- **The Scheduler** periodically polls to see if any DAGs that are registered in the MetaStore need to be executed.
If a particular DAG needs to be triggered (based off the DAGs Schedule), then the Scheduler Daemon **creates a DagRun instance** in the MetaStore and starts to trigger the individual tasks in the DAG.
The scheduler will do this by pushing messages into the Queueing Service.
Each message contains information about the Task it is executing including:
  - the DAG Id
  - Task Id
  - what function needs to be performed.
In the case where the Task is a BashOperator with some bash code, the message will contain this bash code.

- A user might also interact with **the Web Server** and manually trigger DAGs to be ran.
When a user does this, a **DagRun will be created and the scheduler will start to trigger individual Tasks** in the DAG in the same way that was mentioned in #1.

- The celeryd processes controlled by **the Worker daemon**, will pull from the Queueing Service on regular intervals to see if there are any tasks that need to be executed.
When one of the celeryd processes pulls a Task message, **it updates the Task instance in the MetaStore to a Running state and tries to execute the code provided**.
If it succeeds then it updates the state as succeeded but if the code fails while being executed then it updates the Task as failed.


### Airflow. Multinode setup:
![multinode_image](./img/WORKFLOW/Airflow_Multi_Node_Setup.PNG)

A more formal setup for Apache Airflow is to distribute the daemons across multiple machines as a cluster.

- Benefits:
  - Higher Availability:
    If one of the worker nodes were to go down or be purposely taken offline, the cluster would still be operational and tasks would still be executed.

  - Distributed Processing:
    If you have a workflow with several memory intensive tasks, then the tasks will be better distributed to allow for higher utilizaiton of data across the cluster and provide faster execution of the tasks.

- Scaling Workers
  - Horizontally:
    You can scale the cluster horizontally and distribute the processing by adding more executor nodes to the cluster and allowing those new nodes to take load off the existing nodes. Since workers don’t need to register with any central authority to start processing tasks, the machine can be turned on and off without any downtime to the cluster.

  - Vertically:
    You can scale the cluster vertically by increasing the number of celeryd daemons running on each node. 

### Airflow. Scaling master nodes:

![scaling_master_nodes](./img/WORKFLOW/Airflow_Scaling_Master_Nodes.PNG)

You can also **add more Master Nodes to your cluster** to scale out the services that are running on the Master Nodes.
This will mainly allow you to scale out the Web Server Daemon incase there are too many HTTP requests coming for one machine to handle or if you want to provide Higher Availability for that service.

One thing to note is that there can only be one Scheduler instance running at a time.
If you have multiple Schedulers running, there is a possibility that **multiple instances of a single task will be scheduled**.
*This could cause some major problems with your Workflow and cause **duplicate data to show up in the final table** if you were running some sort of ETL process.*

*If you would like, the Scheduler daemon may also be setup to run on its own dedicated Master Node.*


### Airflow concepts:

- DAG
  - Directed Acyclic Graph is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies.

- Scope
  - Airflow will load any DAG object it can import from a DAG file. Critically, that means the DAG must appear in globals().

- Default Arguments
  - If a dictionary of default_args is passed to a DAG, it will apply them to any of its operators. This makes it easy to apply a common parameter to many operators without having to type it many times.

- Operators
  - Airflow provides operators for many common tasks, including:
    - BashOperator - executes a bash command
    - PythonOperator - calls an arbitrary Python function
    - EmailOperator - sends an email
    - HTTPOperator - sends an HTTP request
    - MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, etc. - executes a SQL command
    - Sensor - waits for a certain time, file, database row, S3 key, etc…

    - In addition to these basic building blocks, there are many more specific operators:
      - DockerOperator
      - HiveOperator
      - S3FileTransferOperator
      - PrestoToMysqlOperator
      - SlackOperator
      - etc.

- DAG Assignment
  - Operators do not have to be assigned to DAGs immediately (previously dag was a required argument). However, once an operator is assigned to a DAG, it can not be transferred or unassigned. DAG assignment can be done explicitly when the operator is created, through deferred assignment, or even inferred from other operators.

- Tasks
  - Once an operator is instantiated, it is referred to as a “task”. The instantiation defines specific values when calling the abstract operator, and the parameterized task becomes a node in a DAG.

- Task Instances
  - A task instance represents a specific run of a task and is characterized as the combination of a dag, a task, and a point in time. Task instances also have an indicative state, which could be:
    - "running”
    - “success”
    - “failed”
    - “skipped”
    - “up for retry”
    - etc.

- Workflows
  - By combining DAGs and Operators to create TaskInstances, you can build complex workflows


### Pipeline definition example:

---

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('tutorial', default_args=default_args)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)
```
---

- Importing Modules
  - An Airflow pipeline is just a Python script that happens to define an Airflow DAG object.   Let’s start by importing the libraries we will need.

- Default Arguments
  - We’re about to create a DAG and some tasks, and we have the choice to explicitly pass a set of arguments to each task’s constructor (which would become redundant), or (better!) we can define a dictionary of default parameters that we can use when creating tasks.

- Instantiate a DAG
  - We’ll need a DAG object to nest our tasks into. Here we pass a string that defines the dag_id, which serves as a unique identifier for your DAG. We also pass the default argument dictionary that we just defined and define a schedule_interval of 1 day for the DAG.

- Tasks
  - Tasks are generated when instantiating operator objects. An object instantiated from an operator is called a constructor. The first argument task_id acts as a unique identifier for the task.

- Templating with Jinja
  - Airflow leverages the power of Jinja Templating and provides the pipeline author with a set of built-in parameters and macros. Airflow also provides hooks for the pipeline author to define their own parameters, macros and templates.

- Setting up Dependencies
  - We have two simple tasks that do not depend on each other.


## Jenkins

### Jenkins Pipeline:

- It's a suite of plugins which supports implementing and
integrating continuous delivery pipelines into Jenkins.

*Pipeline provides an extensible set of tools for modeling simple-to-complex delivery pipelines «as code» via the Pipeline DSL*

**A continuous delivery (CD) pipeline** - is an automated expression of your process for getting software from version control right through to your users and customers.
This process involves building the software in a reliable and repeatable manner, as well as progressing the built software through multiple stages of testing and deployment.


**Jenkins is, fundamentally, an automation engine which supports a number of automation patterns.**
Pipeline adds a powerful set of automation tools onto Jenkins, supporting use cases that span from simple continuous integration to comprehensive CD pipelines.
By modeling a series of related tasks, users can take advantage of the many features of Pipeline *(code, durable, pausable, versatile, extensible)*

**Building on the core Jenkins value of extensibility, Pipeline is also extensible both by users with Pipeline Shared Libraries and by plugin developers.**



### Features of Pipeline:

- Code:
  - Pipelines are implemented in code and typically checked into source control, giving teams the ability to edit, review, and iterate upon their delivery pipeline.

- Durable:
  - Pipelines can survive both planned and unplanned restarts of the Jenkins master.

- Pausable:
  - Pipelines can optionally stop and wait for human input or approval before continuing the Pipeline run.

- Versatile:
  - Pipelines support complex real-world CD requirements, including the ability to fork/join, loop, and perform work in parallel.

- Extensible:
  - The Pipeline plugin supports custom extensions to its DSL and multiple options for integration with other plugins.


### Pipeline concepts:

- **Pipeline** - is a user-defined model of a CD pipeline.
  - Also, a pipeline block is a key part of Declarative Pipeline syntax.

- **Node** - is a machine which is part of the Jenkins environment and is capable of executing a Pipeline.
  - Also, a node block is a key part of Scripted Pipeline syntax.

- **Stage block** - defines a conceptually distinct subset of tasks performed through the entire Pipeline (e.g. "Build", "Test" and "Deploy" stages), which is used by many plugins to visualize or present Jenkins Pipeline status/progress.

- **Step** - is a single task. Fundamentally, a step tells Jenkins what to do at a particular point in time.
  - For example, to execute the shell command make use the sh step:
    - ```sh 'make'```


### Declarative vs scripted Pipeline syntax:

- Declarative Pipeline:

---  

```js
pipeline {
  agent any stages {      // 1
    stage('Build') {      // 2
      steps {
          sh 'make'       // 3
      }
    }
    stage('Test'){        // 4
      steps {
        sh 'make check'   // 5
        junit 'reports/**/*.xml'
      }
    }
    stage('Deploy') {     // 6
      steps {
        sh 'make publish' // 7
      }
    }
  }
} 
```
*In Declarative Pipeline syntax, the pipeline block defines all the work done throughout your entire Pipeline*


Code description:
1. Execute this Pipeline or any of its stages, on any available agent.
2. Defines the "Build" stage.
3. Perform some steps related to the "Build" stage.
4. Defines the "Test" stage.
5. Perform some steps related to the "Test" stage.
6. Defines the "Deploy" stage.
7. Perform some steps related to the "Deploy" stage.


---

- Scripted Pipeline:

---

```js
  node {                  // 1
    stage('Build') {      // 2
        sh 'make'         // 3
    }

    stage('Test') {       // 4
        sh 'make check'   // 5
        junit 'reports/**/*.xml'
    }

    stage('Deploy') {     // 6
        sh 'make publish' // 7
    }
}
```
---

**Scripted Pipeline fundamentals**

In Scripted Pipeline syntax, one or more node blocks do/es the core work throughout the entire Pipeline.
Although this is not a mandatory requirement of Scripted Pipeline syntax, confining your Pipeline’s work inside of a node block does two things:
- Schedules the steps contained within the block to run by adding an item to the Jenkins queue.
As soon as an executor is free on a node, the steps will run.

- Creates a workspace (a directory specific to that particular Pipeline) where work can be done on files checked out from source control.

*Code description*:
1. Execute this Pipeline or any of its stages, on any available agent.
2. Defines the "Build" stage. stage blocks are optional in Scripted Pipeline syntax. However, implementing stage blocks in a Scripted Pipeline provides clearer visualization of each stage's subset of tasks/steps in the Jenkins UI.
3. Perform some steps related to the "Build" stage.
4. Defines the "Test" stage.
5. Perform some steps related to the "Test" stage.
6. Defines the "Deploy" stage.
7. Perform some steps related to the "Deploy" stage.

*Be aware that both stages and steps (above) are common elements of both Declarative and Scripted Pipeline syntax*












# NOSQL

## NoSQL Overview

| metric             | SQL                                           | NoSQL                                                                                |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------ |
| type               | Relational                                    | Non-Relational                                                                       |
| data               | Structured Data stored in Tables              | Un-structured stored in JSON files but the graph database does supports relationship |
| schema             | Static                                        | Dynamic                                                                              |
| scalability        | Vertical                                      | Horizontal                                                                           |
| language           | Structured Query Language                     | Un-structured Query Language                                                         |
| joins              | Helpful                                       | No joins, Don't have the powerful interface to prepare complex query                 |
| OLTP               | Recommended and best suited for OLTP systems  | Less likely to be considered for OLTP system                                         |
| support            | Great support                                 | community dependent, they are expanding the support model                            |
| integrated caching | Supports In-line memory(SQL2014 and SQL 2016) | Supports integrated caching                                                          |
| flexible           | rigid schema bound to relationship            | Non-rigid schema and flexible                                                        |
| transactional      | ACID                                          | CAP theorem                                                                          |
| auto elasticly     | Requires downtime in most cases               | Automatic, No outage required                                                        |

### CAP Theorem:

![NOSQL_CAP_theorem](./img/NOSQL/NOSQL_CAP_Theorem.PNG)

**The theorem states that within a largescale data system, there are three requirements that have a relationship of sliding dependency:**
- **Consistency: all clients will read the same value for the same query, even given concurrent update**
- **Availability: all clients will always be able to read and write data**
- **Partition tolerance: the database can be split into multiple machines; it can continue functioning is the face of network segmentation breaks**

*Brewer’s theorem is that in any given system, **you can strongly support only two of the three***

*When choosing a data management system you must balance between: consistency, availability, and partition tolerance:*
- *Consistency means that each client always has the same view of the data;*
- *Availability means that all clients can always read and write;*
- *Partition tolerance means that the system works well across physical network partitions.*

#### Consistent, Available (CA) Systems:
*have trouble with partitions and typically deal with it with the help of replication. Examples of CA systems are:*
- Traditional RDBMSs like Postgres, MySQL, etc (relational)
- Vertica (column-oriented)
- Aster Data (relational)
- Greenplum (relational)

#### Consistent, Partition-Tolerant (CP) Systems:
*have trouble with availability while keeping data consistent across partitioned nodes. Examples of CP systems are:*
- BigTable (column-oriented/tabular)
- HBase (column-oriented/tabular)
- MongoDB (document-oriented)
- Terrastore (document-oriented)
- Redis (key-value)


#### Available, Partition-Tolerant (AP) Systems:
*achieve “eventual consistency” through replication and verification. Examples of AP systems include:*
- Voldemort (key-value)
- KAI (key-value)
- Cassandra (column-oriented/tabular)
- CouchDB (document-oriented)
- Riak (document-oriented)

### NoSQL DB types:
- SQL/New SQL
- Document Databases
- Column Based Databases
- Key/Value Databases
- Graph Databases
- Resource Storages

#### SQL Databases:

**A relational database** - is a digital database whose organization is based on the relational model of data.
Virtually **all relational database systems use SQL** (Structured Query Language) as the language for querying and maintaining the database.
This model organizes data into one or more tables (or "relations") of columns and rows, with a unique key identifying each row. Rows are also called records or tuples

Features:
- Standard de facto over decades
- SQL is great
- Proven approach
- ACID
- Limited scale
- Good fail tolerance

#### Document Databases:

Designed for storing, retrieving, and managing document-oriented information, also known as semistructured data.
**Document databases store all information for a given object in a single instance in the database, and every stored object can be different from every other**, this makes document stores attractive for programming web applications

Features:
- Good for domain object storage
- Good scalability
- Simple API
- Most common substitution of SQL
- Limited consistency
- Large volume support
- Flexible schema

#### Column Databases:

Stores data tables as columns rather than as rows.
Columnar databases become the backbone in a system to serve data for common ETL and data visualization tools.
*The database can more precisely access the data it needs to answer a query rather than scanning and discarding unwanted data in rows.*

Features:
- Good performance
- Great for analytics
- Data compactness
- Flexible schema
- Great scalability
- Limited consistency
- Specific data modeling

#### Key/Value Databases:

A key-value store, or key-value database, is a data storage paradigm designed for storing, retrieving, and managing associative arrays, a data structure more commonly known today as a dictionary or hash.
Dictionaries contain a collection of objects, or records, which in turn have many different fields within them, each containing data.
**These records are stored and retrieved using a key that uniquely identifies the record, and is used to quickly find the data within the database.**

Features:
- Great performance
- Great scalability
- Limited data modeling
- Simple querying only
- Great for cache
- Simple for usage

#### Graph Databases:

Graph database is a database that uses graph structures for semantic queries with nodes, edges and properties to represent and store data.
**A key concept of the system is the graph(or edge or relationship), which directly relates data items in the store.**
**The relationships allow data in the store to be linked together directly, and in most cases retrieved with a single operation. This contrasts**

Features:
- Great join performance
- Best for connected data
- Advanced join querying
- Bad for volume
- Great for analytics
- Specific data model
- Not silver bullet


### POLYGLOT PERSITENCE
- Real life
- Effectiveness
- Complexity
- Micro services
- High volumes

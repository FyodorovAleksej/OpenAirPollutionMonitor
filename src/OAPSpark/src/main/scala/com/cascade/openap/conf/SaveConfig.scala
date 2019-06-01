package com.cascade.openap.conf

class SaveConfig(val format: String,
                 val path: String,
                 val mode: String,
                 val partition: Option[String] = None,
                 val bucketing: Option[String] = None,
                 val bucket_count: Option[Int] = None)

object SaveConfig {
  def apply(format: String,
            path: String,
            mode: String,
            partition: Option[String] = None,
            bucketing: Option[String] = None,
            bucket_count: Option[Int] = None): SaveConfig = new SaveConfig(format, path, mode, partition, bucketing, bucket_count)

  def parseFormLines(lines: Seq[String]): SaveConfig = {
    val temp = lines.filter(_.contains(":"))
    val splited = temp.map(_.split(":", 1))
    val values = splited.map(x => (prepare(x(0).toUpperCase()), prepare(x(1)))).toMap

    new SaveConfig(
      values("FORMAT"),
      values("PATH"),
      values("MODE"),
      values.get("PARTITION"),
      values.get("BUCKETING"),
      values.get("BUCKET_COUNT") match {
        case Some(x) => Some(x.toInt)
        case None => None
      })
  }

  def prepare(strLine: String): String = {
    var line = strLine
    if (line.startsWith(" ") || line.startsWith("\t") || line.startsWith("\n")) {
      line = line.substring(1)
    }
    else if (line.endsWith(" ") || line.endsWith("\t") || line.endsWith("\n")) {
      line = line.substring(0, line.length - 1)
    }
    line
  }
}

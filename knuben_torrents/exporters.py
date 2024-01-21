import scrapy
from datetime import datetime
from scrapy.exporters import XmlItemExporter


class KnubenTorrentsReleasesRSSExporter(XmlItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs["root_element"] = "rss"
        kwargs["item_element"] = "item"
        self.channel_element = "channel"
        self.item_element = "item"

        now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S %z")
        self.title = "Knuben RSS"
        self.link = "https://rss.knuben.eu/1080///hidexxx"
        self.description = "Knuben RSS feed"
        self.language = "en-us"
        self.build_date = now

        super(KnubenTorrentsReleasesRSSExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        self.xg.startDocument()
        self.xg.startElement(
            self.root_element,
            {
                "version": "2.0",
            },
        )
        self._beautify_newline()
        self._beautify_indent(1)
        self.xg.startElement(self.channel_element, {})
        self._beautify_newline()

        self._export_xml_field("title", self.title, depth=2)
        self._export_xml_field("link", self.link, depth=2)
        self._export_xml_field("description", self.description, depth=2)
        self._export_xml_field("pubDate", self.build_date, depth=2)
        self._export_xml_field("lastBuildDate", self.build_date, depth=2)
        self._beautify_newline(new_item=True)

    def export_item(self, item):
        self._beautify_indent(depth=2)
        self.xg.startElement(self.item_element, {})
        self._beautify_newline()

        self._export_xml_field("title", item.get("name"), depth=3)
        self._export_xml_field("link", item.get("magnet"), depth=3)
        self._export_xml_field("description", item.get("description"), depth=3)
        self._export_xml_field("pubDate", item.get("date"), depth=3)
        self._export_xml_field("guid", item.get("url"), depth=3)

        self._beautify_indent(depth=2)
        self.xg.endElement(self.item_element)
        self._beautify_newline(new_item=True)

    def finish_exporting(self):
        self.xg.endElement(self.channel_element)
        self.xg.endElement(self.root_element)
        self.xg.endDocument()
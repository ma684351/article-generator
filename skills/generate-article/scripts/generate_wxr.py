import json
import sys
from datetime import datetime, timezone

WXR_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/commentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>
  <channel>
    <title>WordPress Export</title>
    <link>http://localhost</link>
    <description>WordPress Export Channel</description>
    <language>ja</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <item>
      <title>{title}</title>
      <dc:creator><![CDATA[admin]]></dc:creator>
      <description></description>
      <content:encoded><![CDATA[{content}]]></content:encoded>
      <wp:post_id>1</wp:post_id>
      <wp:post_date><![CDATA[{post_date}]]></wp:post_date>
      <wp:post_date_gmt><![CDATA[{post_date_gmt}]]></wp:post_date_gmt>
      <wp:comment_status><![CDATA[open]]></wp:comment_status>
      <wp:ping_status><![CDATA[open]]></wp:ping_status>
      <wp:post_name>{slug}</wp:post_name>
      <wp:status><![CDATA[publish]]></wp:status>
      <wp:post_parent>0</wp:post_parent>
      <wp:menu_order>0</wp:menu_order>
      <wp:post_type><![CDATA[post]]></wp:post_type>
      <wp:post_password><![CDATA[]]></wp:post_password>
      <wp:is_sticky>0</wp:is_sticky>
      <category domain="category" nicename="{category_slug}"><![CDATA[{category_name}]]></category>
    </item>
  </channel>
</rss>
"""

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_wxr.py <input.json> <output.xml>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 必須キーの確認
        required_keys = ['title', 'slug', 'category_name', 'category_slug', 'content']
        for key in required_keys:
            if key not in data:
                print(f"Error: JSONファイルに必須キー '{key}' が含まれていません。")
                sys.exit(1)

        # 現在時刻をダミーの投稿日として使用
        now = datetime.now(timezone.utc)
        post_date = now.strftime("%Y-%m-%d %H:%M:%S")
        post_date_gmt = now.strftime("%Y-%m-%d %H:%M:%S")

        xml_content = WXR_TEMPLATE.format(
            title=data['title'],
            content=data['content'],
            slug=data['slug'],
            category_name=data['category_name'],
            category_slug=data['category_slug'],
            post_date=post_date,
            post_date_gmt=post_date_gmt
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"✅ WXRファイルを生成しました: {output_file}")

    except Exception as e:  # noqa: BLE001
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import os
import requests
from bs4 import BeautifulSoup

# 创建保存文件夹
save_folder = "pdf_files"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


# 爬取网页函数
def fetch_page(page_number):
    # 构建页面 URL（根据提供的链接进行递增）
    url = f"https://www.nsfocus.com.cn/html/7/20/{page_number}.html"

    # 请求网页，使用 verify=False 跳过 SSL 证书验证
    response = requests.get(url, verify=False)

    # 如果网页请求成功
    if response.status_code == 200:
        print(f"成功请求网页: {url}")
        # 确保使用 UTF-8 解码网页内容
        response.encoding = 'utf-8'
        return response.text
    else:
        print(f"请求失败: {url}")
        return None


# 遍历网页的函数
def crawl_pages(start, end):
    for page_number in range(start, end + 1):
        print(f"正在处理第 {page_number} 页...")
        page_content = fetch_page(page_number)

        if page_content:
            # 在此处可以进行进一步的处理，例如解析 HTML 并下载 PDF 文件
            parse_page(page_content, page_number)
        else:
            print(f"跳过第 {page_number} 页，因为请求失败。")


# 解析页面内容，定位到指定的 <div> 标签区域
def parse_page(page_content, page_number):
    soup = BeautifulSoup(page_content, "html.parser")

    # 查找 <div class="wrap_c zyzx_main_box">
    wrap_c_div = soup.find("div", class_="wrap_c zyzx_main_box")

    # 如果找到了该区域
    if wrap_c_div:
        print("找到了指定区域，正在提取内容...")

        # 提取所有 <p class="p1"> 标签中的期号信息
        p_tags = wrap_c_div.find_all("p", class_="p1")
        for p_tag in p_tags:
            # 使用 UTF-8 解码确保文件名不会乱码
            file_name = p_tag.get_text(strip=True).encode('utf-8').decode('utf-8')
            print(f"提取的文件名: {file_name}")

            # 查找 <a> 标签中包含 PDF 下载链接的 href
            download_link = wrap_c_div.find("a", class_="a1", href=True)
            if download_link:
                pdf_url = download_link["href"]
                full_pdf_url = "https://www.nsfocus.com.cn" + pdf_url  # 补全 URL
                print(f"找到 PDF 下载链接: {full_pdf_url}")

                # 下载 PDF 文件
                download_pdf(full_pdf_url, file_name)
            else:
                print("未找到下载链接。")
    else:
        print("未找到指定区域")


# 下载 PDF 文件的函数
def download_pdf(pdf_url, file_name):
    try:
        pdf_response = requests.get(pdf_url, verify=False)  # 添加 verify=False 参数跳过 SSL 证书验证
        if pdf_response.status_code == 200:
            # 保存 PDF 文件，确保文件名不会乱码
            file_path = os.path.join(save_folder, file_name + ".pdf")
            with open(file_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"成功下载 PDF 文件: {file_name}.pdf")
        else:
            print(f"PDF 下载失败: {pdf_url}")
    except Exception as e:
        print(f"下载时发生错误: {e}")


# 设置爬取页面的范围，从第 2 页到第 10 页
crawl_pages(1, 10)

import requests
from bs4 import BeautifulSoup
import re
import os
from opencc import OpenCC
from tqdm import tqdm
import cv2
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time


keywords = ['凤凰卫视', '人间卫视', '香港卫视', '翡翠台', '凤凰香港', '凤凰中文', '凤凰资讯', 'AMC电影台', '电影台', '大爱', '东森', '好莱坞', '纬来', '天映', '八大', 
            '华视', '中天', '天良', '美亚', '星影', '无线', '华剧台', '华丽台', '采昌', '靖天', '民视', '三立', '影视2', 
            '影视3', '中视', '豬哥亮', 'TVB', '公视', '寰宇', '戏剧台', '靖天', '靖洋', '龙华', '龙祥', '猪哥亮', '影迷', '影剧', '台视', '华视', 
            '中华小当家', '中天娱乐', '公视戏剧', '动漫', '动物星球', '动画台', '壹新闻', '大立电视', '天良', '探案', '超人', '番薯']  # 这里定义你的搜索关键词列表
output_file = 'gat.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for keyword in keywords:
        url = f'http://tonkiang.us/?&iqtv={keyword}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            f.write(text_content + '\n')
        else:
            print(f'请求 {url} 失败，状态码：{response.status_code}')
        time.sleep(1)  # 添加 1 秒的延迟

            
with open('gat.txt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines
new_lines = []
for i in range(len(lines)):
    line = lines[i]
    if 'http' in line:
        # 找到当前行之前的非空行作为频道名称
        for j in range(i - 1, -1, -1):
            if lines[j].strip():
                channel_name = lines[j].strip()
                break
        channel_url = line.strip()
        new_lines.append(f'{channel_name},{channel_url}\n')
with open('gat.txt', 'w', encoding='utf-8') as outfile:
    outfile.writelines(new_lines)

keywords = ['凤凰卫视', '人间卫视', '香港卫视', '翡翠台', '凤凰香港', '凤凰中文', '凤凰资讯', '电影台', '电影台', '大爱', '东森', '好莱坞', '纬来', '天映', '八大',
            '华视', '中天', '天良', '美亚', '星影', '无线', '华剧台', '华丽台', '采昌', '靖天', '民视', '三立', '中视', '猪哥亮', 'TVB', '公视', '寰宇', '戏剧台', '靖天', '靖洋', '龙华', '龙祥', '猪哥亮', '影迷', '影剧', '台视', '华视',
            '中华小当家', '中天娱乐', '公视戏剧', '动漫', '动物星球', '动画台', '壹新闻', '大立电视', '天良', '探案', '超人', '番薯']  # 这里定义你的搜索关键词列表
output_file = '2.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for keyword in keywords:
        url = f'https://api.pearktrue.cn/api/tv/search.php?name={keyword}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(response.content)  # 打印响应内容
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text_content = soup.get_text()
                    f.write(text_content + '\n')
                except Exception as e:
                    print(f"Error parsing content for keyword {keyword}: {e}")
            else:
                print(f'请求 {url} 失败，状态码：{response.status_code}')
        except Exception as e:
            print(f"Error fetching URL for keyword {keyword}: {e}")
        time.sleep(1)  # 添加 1 秒的延迟

result = []
with open('2.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if '"videoname":' in line:
            videoname_start = line.find('"videoname":') + len('"videoname": "')
            videoname_end = line.find('",', videoname_start)
            videoname = line[videoname_start:videoname_end]
        elif '"link":' in line:
            link_start = line.find('"link":') + len('"link": "')
            link_end = line.find('"', link_start)
            link = line[link_start:link_end]
            result.append(f"{videoname},{link}\n")

with open('gat.txt', 'a', encoding='utf-8') as f:
    f.writelines(result)


def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))

# 使用方法
remove_duplicates('gat.txt', 'gat.txt')
print("处理完成，去重完成")




################简体转繁体
# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('gat.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入txt文件
with open('gat.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)
print("处理完成，繁体转换完成")


######################################################################################提取goodiptv
import re
import os
# 定义一个包含所有要排除的关键词的列表
excluded_keywords = ['zhoujie218', 'service', '112114', 'xfjcHD', 'stream8.jlntv', 'live.cooltv', 'P2P', '新闻综合', 'P3p', 'cookies', '9930/qilu', 'gitcode.net']   #, '', ''
# 定义一个包含所有要提取的关键词的列表
extract_keywords = [',']
# 读取文件并处理每一行
with open('gat.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    # 创建或打开一个输出文件用于写入处理后的数据
    with open('gat.txt', 'w', encoding='utf-8') as outfile:
        for line in lines:
            # 首先检查行是否包含任何提取关键词
            if any(keyword in line for keyword in extract_keywords):
                # 如果包含提取关键词，进一步检查行是否不包含任何排除关键词
                if not any(keyword in line for keyword in excluded_keywords):
                    outfile.write(line)  # 写入符合条件的行到文件




def filter_lines(file_path):
    with open('gat.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    filtered_lines = []
    for line in lines:
        if ',' in line:
         if 'epg' not in line and 'mitv' not in line and 'udp' not in line and 'rtp' not in line and '[' not in line \
            and 'P2p' not in line and 'p2p' not in line and 'p3p' not in line and 'P2P' not in line and 'P3p' not in line and 'P3P' not in line:
          filtered_lines.append(line)
    
    return filtered_lines

def write_filtered_lines(output_file_path, filtered_lines):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(filtered_lines)

if __name__ == "__main__":
    input_file_path = 'gat.txt'
    output_file_path = "gat.txt"
    
    filtered_lines = filter_lines(input_file_path)
    write_filtered_lines(output_file_path, filtered_lines)

print("/" * 80)






# ###########################################定义替换规则的字典,对整行内的内容进行替换
replacements = {
        " ": "",
}

# 打开原始文件读取内容，并写入新文件
with open('gat.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建新文件并写入替换后的内容
with open('gat.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():
            line = line.replace(old, new)
        new_file.write(line)   
######################连通性检测
import requests
import queue
import threading
from tqdm import tqdm
def test_connectivity(url, max_attempts=2):
    for _ in range(max_attempts):
        try:
            response = requests.head(url, timeout=3)
            return response.status_code == 200
        except requests.RequestException:
            pass
    return False
def process_line(line, result_queue):
    parts = line.strip().split(",")
    if len(parts) == 2 and parts[1]:
        channel_name, channel_url = parts
        if test_connectivity(channel_url):
            result_queue.put((channel_name, channel_url))
    else:
        pass
def main(source_file_path, output_file_path):
    with open(source_file_path, "r", encoding="utf-8") as source_file:
        lines = source_file.readlines()
    result_queue = queue.Queue()
    threads = []
    for line in tqdm(lines, desc="检测进行中"):
        thread = threading.Thread(target=process_line, args=(line, result_queue))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        while not result_queue.empty():
            item = result_queue.get()
            if item[0] and item[1]:
                output_file.write(f"{item[0]},{item[1]}\n")
if __name__ == "__main__":
    try:
        source_file_path = "gat.txt"
        output_file_path = "gat.txt"
        main(source_file_path, output_file_path)
    except Exception as e:
        print(f"程序发生错误: {e}")




########################## 函数：获取视频分辨率
def get_video_resolution(video_path, timeout=0.8):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return (width, height)
# 函数：处理每一行
def process_line(line, output_file, order_list, valid_count, invalid_count, total_lines):
    parts = line.strip().split(',')
    if '#genre#' in line:
        # 如果行包含 '#genre#'，直接写入新文件
        with threading.Lock():
            output_file.write(line)
            print(f"已写入genre行：{line.strip()}")
    elif len(parts) == 2:
        channel_name, channel_url = parts
        resolution = get_video_resolution(channel_url, timeout=8)
        if resolution and resolution[1] >= 720:  # 检查分辨率是否大于等于720p
            with threading.Lock():
                output_file.write(f"{channel_name}[{resolution[1]}p],{channel_url}\n")
                order_list.append((channel_name, resolution[1], channel_url))
                valid_count[0] += 1
                print(f"Channel '{channel_name}' accepted with resolution {resolution[1]}p at URL {channel_url}.")
        else:
            invalid_count[0] += 1
    with threading.Lock():
        print(f"有效: {valid_count[0]}, 无效: {invalid_count[0]}, 总数: {total_lines}, 进度: {(valid_count[0] + invalid_count[0]) / total_lines * 100:.2f}%")
# 函数：多线程工作
def worker(task_queue, output_file, order_list, valid_count, invalid_count, total_lines):
    while True:
        try:
            line = task_queue.get(timeout=1)
            process_line(line, output_file, order_list, valid_count, invalid_count, total_lines)
        except Queue.Empty:
            break
        finally:
            task_queue.task_done()

# 主函数
def main(source_file_path, output_file_path):
    order_list = []
    valid_count = [0]
    invalid_count = [0]
    task_queue = Queue()
    # 读取源文件
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()
    with open(output_file_path + '.txt', 'w', encoding='utf-8') as output_file:
        # 创建线程池
        with ThreadPoolExecutor(max_workers=64) as executor:
            # 创建并启动工作线程
            for _ in range(128):
                executor.submit(worker, task_queue, output_file, order_list, valid_count, invalid_count, len(lines))
            # 将所有行放入队列
            for line in lines:
                task_queue.put(line)
            # 等待队列中的所有任务完成
            task_queue.join()
    print(f"任务完成，有效频道数：{valid_count[0]}, 无效频道数：{invalid_count[0]}, 总频道数：{len(lines)}")
if __name__ == "__main__":
    source_file_path = 'gat.txt'  # 替换为你的源文件路径
    output_file_path = 'gat'  # 替换为你的输出文件路径,不要后缀名
    main(source_file_path, output_file_path)
# 无需再打印酒店源，因为这里是对所有URL进行检测，而不是基于IP分组检测



with open('gat.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()

lines.sort()

with open('gat.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)



import re
from pypinyin import lazy_pinyin

# 打开一个utf-8编码的文本文件
with open("gat.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))
# 将排序后的行写入新的utf-8编码的文本文件
with open("gat.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)


from pypinyin import lazy_pinyin
import re
import os
from opencc import OpenCC
import fileinput
########################################################################################################################################################################################
########################################## 打开用户指定的文件打开用户指定的文件打开用户指定的文件
with open("gat.txt", 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
# ###########################################定义替换规则的字典对频道名替换
replacements = {
    	"CCTV-1高清测试": "",
    	"CCTV-2高清测试": "",
    	"CCTV-7高清测试": "",
    	"CCTV-10高清测试": "",
    	"中央": "CCTV",
    	"高清""": "",
    	"HD": "",
    	"[浙江]": "浙江",
    	"|": "",
    	"」": "",
    	"标清": "",
    	"-": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"[1080p]": "",
    	"[720p]": "",
    	"[540p]": "",
    	"[576p]": "",
    	"[720*480]": "",
    	"[1280*720]": "",
    	"[1920*1080]": "",
    	"[960*540]": "",
    	"SD": "",
    	"「": "",
    	"IPV6": "",
    	"3.5M1080": "",
    	"5M1080HEVC": "",
    	"5.5M1080HEVC": "",
    	"8M1080": "",
    	"4M1080": "",
    	"｜": "",
    	"[2160p]": "",
    	"1080p": "",
    	"720p": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"超清": "",
    	"湖南金鹰纪实": "金鹰纪实",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	" ": "",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV兵器科技": "兵器科技",
    	"CCTV地理世界": "地理世界",
    	"CCTV风云足球": "风云足球",
    	"CCTV央视台球": "央视台球",
    	"CCTV台球": "台球",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV中视购物": "中视购物",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"熊猫影院": "熊猫电影",
    	"熊猫爱生活": "熊猫生活",
    	"爱宠宠物": "宠物生活",
    	"[ipv6]": "",
    	"专区": "",
    	"卫视超": "卫视",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"IPTV": "",
    	"PLUS": "+",
    	"＋": "+",
    	"(": "",
    	")": "",
    	"CAV": "",
    	"美洲": "",
    	"北美": "",
    	"12M": "",
    	"高清测试CCTV-1": "",
    	"高清测试CCTV-2": "",
    	"高清测试CCTV-7": "",
    	"高清测试CCTV-10": "",
    	"LD": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	"NewTv": "",
    	"NEWTV": "",
    	"NewTV": "",
    	"iHOT": "",
    	"CHC": "",
    	"测试cctv": "CCTV",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"CCTV4国际": "CCTV4",
    	"CCTV4中文国际": "CCTV4",
    	"CCTV4欧洲": "CCTV4",
    	"CCTV5体育": "CCTV5",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV6电影": "CCTV6",
    	"CCTV7军事": "CCTV7",
    	"CCTV7军农": "CCTV7",
    	"CCTV7农业": "CCTV7",
    	"CCTV7国防军事": "CCTV7",
    	"CCTV8电视剧": "CCTV8",
    	"CCTV8影视": "CCTV8",
    	"CCTV8纪录": "CCTV9",
    	"CCTV9记录": "CCTV9",
    	"CCTV9纪录": "CCTV9",
    	"CCTV10科教": "CCTV10",
    	"CCTV11戏曲": "CCTV11",
    	"CCTV12社会与法": "CCTV12",
    	"CCTV13新闻": "CCTV13",
    	"CCTV新闻": "CCTV13",
    	"CCTV14少儿": "CCTV14",
    	"央视14少儿": "CCTV14",
    	"CCTV少儿超": "CCTV14",
    	"CCTV15音乐": "CCTV15",
    	"CCTV音乐": "CCTV15",
    	"CCTV16奥林匹克": "CCTV16",
    	"CCTV17农业农村": "CCTV17",
    	"CCTV17军农": "CCTV17",
    	"CCTV17农业": "CCTV17",
    	"CCTV5+体育赛视": "CCTV5+",
    	"CCTV5+赛视": "CCTV5+",
    	"CCTV5+体育赛事": "CCTV5+",
    	"CCTV5+赛事": "CCTV5+",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV5赛事": "CCTV5+",
    	"凤凰中文台": "凤凰中文",
    	"凤凰资讯台": "凤凰资讯",
    	"(CCTV4K测试）": "CCTV4K",
    	"上海东方卫视": "上海卫视",
    	"东方卫视": "上海卫视",
    	"内蒙卫视": "内蒙古卫视",
    	"福建东南卫视": "东南卫视",
    	"广东南方卫视": "南方卫视",
    	"湖南金鹰卡通": "金鹰卡通",
    	"炫动卡通": "哈哈炫动",
    	"卡酷卡通": "卡酷少儿",
    	"卡酷动画": "卡酷少儿",
    	"BRTVKAKU少儿": "卡酷少儿",
    	"优曼卡通": "优漫卡通",
    	"优曼卡通": "优漫卡通",
    	"嘉佳卡通": "佳嘉卡通",
    	"世界地理": "地理世界",
    	"CCTV世界地理": "地理世界",
    	"BTV北京卫视": "北京卫视",
    	"BTV冬奥纪实": "冬奥纪实",
    	"东奥纪实": "冬奥纪实",
    	"卫视台": "卫视",
    	"湖南电视台": "湖南卫视",
    	"少儿科教": "少儿",
    	"影视剧": "影视",
    	"电视剧": "影视",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}


# 打开新文本文件准备写入替换后的内容
with open('2.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除行尾的换行符
        line = line.rstrip('\n')
        # 分割行，获取逗号前的字符串
        parts = line.split(',', 1)
        if len(parts) > 0:
            # 替换逗号前的字符串
            before_comma = parts[0]
            for old, new in replacements.items():
                before_comma = before_comma.replace(old, new)
            # 将替换后的逗号前部分和逗号后部分重新组合成一行，并写入新文件
            new_line = f'{before_comma},{parts[1]}\n' if len(parts) > 1 else f'{before_comma}\n'
            new_file.write(new_line)

print("替换完成，新文件已保存。")



########################################################################################################################################################################################
################################################################定义关键词分割规则
def check_and_write_file(input_file, output_file, keywords):
    # 使用 split(', ') 来分割关键词
    keywords_list = keywords.split(',')
    pattern = '|'.join(re.escape(keyword) for keyword in keywords_list)

    # 读取输入文件并提取包含关键词的行
    extracted_lines = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
          if "genre" not in line:
            if re.search(pattern, line):
                extracted_lines.append(line)

    # 如果至少提取到一行，写入头部信息和提取的行到输出文件
    if extracted_lines:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(f"{keywords_list[0]},#genre#\n")  # 写入头部信息
            out_file.writelines(extracted_lines)  # 写入提取的行

        # 获取头部信息的大小
        header_size = len(f"{keywords_list[0]},#genre#\n")
        
        # 检查文件的总大小
        file_size = os.path.getsize(output_file)
        
        # 如果文件大小小于30字节（假设的最小文件大小），删除文件
        if file_size < 20:
            os.remove(output_file)
            print(f"文件只包含头部信息，{output_file} 已被删除。")
        else:
            print(f"文件已提取关键词并保存为: {output_file}")
    else:
        print(f"未提取到关键词，不创建输出文件 {output_file}。")

# 按类别提取关键词并写入文件
check_and_write_file('2.txt','a0.txt',keywords="央视频道,CCTV")
check_and_write_file('2.txt','a.txt',keywords="央视频道,湖北,湖南")
#check_and_write_file('2.txt','a1.txt',keywords="央视频道,动作电影,高清电影,家庭影院,影迷电影")

check_and_write_file('2.txt','c.txt',keywords="影视频道,爱情喜剧,爱喜喜剧,惊嫊悬疑,东北热剧,动作电影,无名,都市剧场,iHOT,海外剧场,欢笑剧场,重温经典,明星大片,中国功夫,军旅,东北热剧,中国功夫,军旅剧场,古装剧场,\
家庭剧场,惊悚悬疑,欢乐剧场,潮妈辣婆,爱情喜剧,精品大剧,超级影视,超级电影,黑莓动画,黑莓电影,海外剧场,精彩影视,无名影视,潮婆辣妈,超级剧,热播精选")
check_and_write_file('2.txt','c1.txt',keywords="影视频道,求索动物,求索,求索科学,求索记录,爱谍战,爱动漫,爱科幻,爱青春,爱自然,爱科学,爱浪漫,爱历史,爱旅行,爱奇谈,爱怀旧,爱赛车,爱都市,爱体育,爱经典,\
爱玩具,爱喜剧,爱悬疑,爱幼教,爱院线")


check_and_write_file('2.txt','e.txt',keywords="港澳频道,TVB,澳门,龙华,民视,中视,华视,AXN,MOMO,采昌,耀才,靖天,镜新闻,靖洋,莲花,年代,爱尔达,好莱坞,华丽,非凡,公视,寰宇,无线,EVEN,MoMo,爆谷,面包,momo,唐人,\
中华小,三立,CNA,FOX,RTHK,Movie,八大,中天,中视,东森,凤凰,天映,美亚,环球,翡翠,亚洲,大爱,大愛,明珠,半岛,AMC,龙祥,台视,1905,纬来,神话,经典都市,视界,番薯,私人,酒店,TVB,凤凰,半岛,星光视界,\
番薯,大愛,新加坡,星河,明珠,环球,翡翠台,ELTV,大立,elta,好消息,美国中文,神州,天良,18台,BLOOMBERG,Bloomberg,CMUSIC,CN卡通,CNBC,CNBC,CinemaWorld,Cinemax,DMAX,Dbox,Dreamworks,ESPN,Euronews,\
Eurosports1,FESTIVAL,GOOD2,HBO家庭,HBO,HISTORY,HOY国际财经,HakkaTV,J2,KOREA,LISTENONSPOTIFY,LUXE,MCE,MTV,Now,PremierSports,ROCK,SPOTV,TiTV,VOA,ViuTV,ViuTV6,WSport,WWE,八度,博斯,达文西,迪士尼,\
动物星球,港石金曲,红牛,互动英语,华纳影视,华语剧台,ELTV,欢喜台,旅游,美食星球,nhkworld,nickjr,千禧,全球财经,探案,探索,小尼克,幸福空间,影剧,粤语片台,智林,猪哥亮")



###############################################################################################################################################################################################################################
##############################################################对生成的文件进行合并
file_contents = []
file_paths = ["a0.txt", "a.txt", "a1.txt", "b0.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "f0.txt", "f.txt", "f1.txt", "g0.txt", "g.txt", "g1.txt", "h0.txt", "h.txt", "h1.txt", "i.txt", \
              "i1.txt", "j.txt", "j1.txt", "k.txt", "l0.txt", "l.txt", "l1.txt", "m.txt", "m1.txt",  \
              "n0.txt","n.txt","n1.txt", "e.txt", "o1.txt", "o.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
    else:                # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file_path} 不存在，跳过")
# 写入合并后的文件
with open("去重.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

###############################################################################################################################################################################################################################
##############################################################对生成的文件进行网址及文本去重复，避免同一个频道出现在不同的类中

def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[https]?[http]?[P2p]?[mitv]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))

# 使用方法
remove_duplicates('去重.txt', 'GAT.txt')

# 打开文档并读取所有行 
with open('GAT.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
 
# 使用列表来存储唯一的行的顺序 
 unique_lines = [] 
 seen_lines = set() 

# 遍历每一行，如果是新的就加入unique_lines 
for line in lines:
 if line not in seen_lines:
  unique_lines.append(line)
  seen_lines.add(line)

# 将唯一的行写入新的文档 
with open('gat.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)





################################################################################################任务结束，删除不必要的过程文件
files_to_remove = ['去重.txt', "2.txt", "a0.txt", "a.txt", "a1.txt", "b0.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "e.txt", "f0.txt", "f.txt", "f1.txt", "g0.txt", "g.txt", "g1.txt", "h0.txt", "h.txt", "h1.txt", "i.txt", \
              "i1.txt", "j.txt", "j1.txt", "k.txt", "l0.txt", "l.txt", "l1.txt", "m.txt", "m1.txt",  \
              "n0.txt","n.txt","n1.txt", "o1.txt", "o.txt", "p.txt"]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")

print("任务运行完毕，GAT频道列表可查看文件夹内综合源.txt文件！")


def append_text_between_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        content1 = file1.read()
        lines1 = content1.split('\n')
        seen = set()
        unique_lines1 = []
        for line in lines1:
            if line not in seen:
                seen.add(line)
                unique_lines1.append(line)
    with open(file2_path, 'r', encoding='utf-8') as file2:
        content2 = file2.read()
        lines2 = content2.split('\n')
        seen = set()
        unique_lines2 = []
        for line in lines2:
            if line not in seen:
                seen.add(line)
                unique_lines2.append(line)
    combined_lines = unique_lines2 + unique_lines1
    with open(file2_path, 'w', encoding='utf-8') as file2:
        file2.write('\n'.join(combined_lines))
file_path1 = 'GAT.txt'
file_path2 = '综合源.txt'
append_text_between_files(file_path1, file_path2)


#TXT转M3U#
import datetime
def txt_to_m3u(input_file, output_file):
    # 读取txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 打开m3u文件并写入内容
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    current_time = now.strftime("%Y/%m/%d %H:%M")
    with open(output_file, 'w', encoding='utf-8') as f:  
        f.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"\n')
        #f.write(f'#EXTINF:-1 group-title="更新时间",请您欣赏\n')    
        #f.write(f'https://vd2.bdstatic.com/mda-nk3am8nwdgqfy6nh/sc/cae_h264/1667555203921394810/mda-nk3am8nwdgqfy6nh.mp4\n')    
        #f.write(f'#EXTINF:-1 group-title="{current_time}",虚情的爱\n')    
        #f.write(f'https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n')    
        # 初始化genre变量
        genre = ''
        # 遍历txt文件内容
        for line in lines:
            line = line.strip()
            if "," in line:  # 防止文件里面缺失",”号报错
                # if line:
                # 检查是否是genre行
                channel_name, channel_url = line.split(',', 1)
                if channel_url == '#genre#':
                    genre = channel_name
                    print(genre)
                else:
                    # 将频道信息写入m3u文件
                    f.write(f'#EXTINF:-1 tvg-logo="https://live.fanmingming.com/tv/{channel_name}.png" group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')
# 将txt文件转换为m3u文件
txt_to_m3u('综合源.txt', '综合源.m3u')


import datetime
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
current_time = now.strftime("%Y/%m/%d %H:%M")   #:%M
# 打开文本文件并将时间添加到开头
file_path = "综合源.m3u"
with open(file_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(f'{content}\n')
    #f.write(f'#EXTINF:-1 group-title="更新时间",请您欣赏\n')    
    #f.write(f'http://em.21dtv.com/songs/60144971.mkv\n')    
    f.write(f'#EXTINF:-1 group-title="{current_time}更新",虚情的爱\n')    
    f.write(f'https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n')   




import datetime
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
current_time = now.strftime("%Y/%m/%d %H:%M")
# 打开文本文件并将时间添加到开头
file_path = "综合源.txt"
with open(file_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(f'{content}\n')
    f.write(f'')
    #f.write(f'请您欣赏,https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n')
    f.write(f'{current_time}更新,#genre#\n')
    f.write(f'虚情的爱,https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n')


     

################################################################################################任务结束，删除不必要的过程文件
files_to_remove = ["gat.txt", "汇总.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
print("任务运行完毕，频道列表可查看文件夹内源.txt文件！")



print("任务运行完毕，GAT频道列表可查看文件夹内综合源.txt文件！")

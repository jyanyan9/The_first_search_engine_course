import os
import torch
import string
from ltp import LTP
import jieba
from pyhanlp import *
import fool
import re
import glob
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
# ------------------
# 文本重命名
# ------------------
def rename(path):
    path_C = './gobug_C/'
    path_E = './gobug_E/'
    i = 1
    if path==path_C:
        name = 'Zh'
    else:
        name = 'En'
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            newname = f'News_{i}_Result_'+ name +'.txt'  # 将文件名修改为数字序列 + 文件扩展名
            os.rename(os.path.join(path, filename), os.path.join(path, newname))
            i += 1
    return i

# ------------------
# 开始进入文本处理阶段
# ------------------
def stand(path):
    if path=="C":
        folder_path = './gobug_C/'
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            # 使用正则表达式删除特殊字符和标点符号
            text = re.sub(r'[^\u4e00-\u9fa5\d]+', '', file_content)
            # 将字符串拆分为单个汉字和数字
            characters = re.findall(r'[\u4e00-\u9fa5\d]', text)
            words = str(characters)
            new_words = words.replace('[', '').replace(']', '').replace('\'', '').replace(',', '').replace(' ', '')
            # 输出结果
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(new_words)
    else:
        folder_path = './gobug_E/'
        # 打开要读取的文件
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            # 使用正则表达式删除标点符号和特殊字符，并将所有大写字母转换为小写字母
            processed_text = re.sub(r'[^\w\s\d]', '', file_content).lower()
        # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(processed_text)
# ------------------
# 开始进入分词阶段
# ------------------
def cut(model):
    folder_path = './gobug_C/'
    if model=='ltp':
        ltp = LTP("LTP/small")  # 默认加载 Small 模型
        # 将模型移动到 GPU 上
        if torch.cuda.is_available():
            # ltp.cuda()
            ltp.to("cuda")
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            words = ltp.pipeline(file_content)[0]
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(' '.join(words))
    elif model=='jieba':
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            words = jieba.cut(file_content,cut_all=False)
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(' '.join(words))
    elif model=='hanlp':
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            words = HanLP.newSegment().enableCustomDictionary(False)
            result = segmenter.seg(file_content)
            words = ''
            for term in result:
                words += term.word + ' '
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(words)
    else:
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            words = str(fool.cut(file_content))
            words = words.replace('[', '').replace(']', '').replace('\'', '').replace(',', '').replace(' ', ' ')
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(words)
# ------------------
# 删除中英停用词
# ------------------
def stop(stopword):
    if stopword=='C':
        folder_path = './gobug_C/'
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                file_content = f.read()
            # 读取停用词表
            stopwords_Zh = [line.strip() for line in open('./stopwords.txt', 'r', encoding='utf-8').readlines()]
            # 删除停用词
            filtered_tokens = str([word for word in file_content if word not in stopwords_Zh])
            words = filtered_tokens.replace('[', '').replace(']', '').replace('\'', '').replace(',', '')
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(words)
    else:
        folder_path = './gobug_E/'
        for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
            with open(filepath, "r", encoding='utf-8') as f:
                # 读取文件内容
                text = f.read()
            # 读取并删除停用词表
            stop_words = set(stopwords.words('english'))
            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
            # 打开要写入的文件
            with open(filepath, "w", encoding='utf-8') as f:
                file_content = f.write(text)
# ----------------------------------
# 实现英文文本的Porter词干提取
# ----------------------------------
def stem():
    folder_path = './gobug_E/'
    for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
        with open(filepath, "r", encoding='utf-8') as f:
            # 读取文件内容
            file_content = f.read()
        # 词干提取
        words = word_tokenize(file_content)
        stemmer = PorterStemmer()
        stemmed_words = str([stemmer.stem(word) for word in words])
        new_words = stemmed_words.replace('[', '').replace(']', '').replace('\'', '').replace(',', '').replace(' ', ' ')
        # 打开要写入的文件
        with open(filepath, "w", encoding='utf-8') as f:
            file_content = f.write(new_words)
# ----------------------------------
# 接下来是主函数
# ----------------------------------
if __name__ == '__main__':
    path_C = './gobug_C/'
    path_E = './gobug_E/'
    print("现在处理的是中文文本")
    stand('C')
    print("现在处理的是英文文本")
    stand('D')
    model = input('请选择中文分词模型(LTP/jieba/HanLP/Foolnltk)：')
    cut(model)
    print("现在删除中文停用词")
    stop('C')
    print("现在删除英文停用词")
    stop('D')
    print("现在进行英文词干提取")
    stem()
    print("现在进行文件重命名")
    rename(path_C)
    rename(path_E)










import os
import comtypes.client

def excelToPDF(in_file, out_file):
    excel = comtypes.client.CreateObject("Excel.Application")
    excel.Visible = 0
    wb = excel.Workbooks.Open(in_file)

    wb.SaveAs(out_file, FileFormat=57)
    wb.Close()
    excel.Quit()
    
def wordToPDF(in_file, out_file):
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=17)
    doc.Close()
    word.Quit()
    
def powerpointToPDF(inputFileName, outputFileName):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, 32)
    deck.Close()
    powerpoint.Quit()

def getFilesInFolder(folder_path):
    result = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path) and not "~$" in full_path:
                result.append((file, full_path))

    return result


print("请输入当前待转换文件存放的文件夹")
docs_path = input()
all_file_path = getFilesInFolder(docs_path)

if len(all_file_path) == 0:
    print("当前待转换文件存放的文件夹内没有任何文件")
    exit

print("请输入目标文件夹")
output_path = input()
if os.path.exists(output_path) == False:
    print("目标文件夹不是有效的文件夹")
    exit

all_count = len(all_file_path)
current_count = 0
target_path = ""

for file_path in all_file_path:
    current_count += 1
    progress_info = f"当前进度{current_count}/{all_count}"
    _, file_extension = os.path.splitext(file_path[1])

    if file_extension.lower() == ".xls" or file_extension.lower() == ".xlsx":
        print(f"当前转换的Excel名称：{file_path[1]}")
        target_path = os.path.join(output_path, file_path[0]).replace(".xlsx", ".pdf").replace(".xls", ".pdf")

        if os.path.exists(target_path):
            print(f"{progress_info}，{file_path[0]}文件已存在，跳过当前文件")
        else:
            excelToPDF(file_path[1], target_path)
            print(f"{progress_info}，{file_path[0]}转换完成")

    elif file_extension.lower() == ".doc" or file_extension.lower() == ".docx":
        target_path = os.path.join(output_path, file_path[0]).replace(".docx", ".pdf").replace(".doc", ".pdf")

        if os.path.exists(target_path):
            print(f"{progress_info}，{file_path[0]}文件已存在，跳过当前文件")
        else:
            wordToPDF(file_path[1], target_path)
            print(f"{progress_info}，{file_path[0]}转换完成")

    elif file_extension.lower() == ".ppt" or file_extension.lower() == ".pptx":
        target_path = os.path.join(output_path, file_path[0]).replace(".pptx", ".pdf").replace(".pptx", ".pdf")

        if os.path.exists(target_path):
            print(f"{progress_info}，{file_path[0]}文件已存在，跳过当前文件")
        else:
            powerpointToPDF(file_path[1], target_path)
            print(f"{progress_info}，{file_path[0]}转换完成")

    else:
        print(f"{progress_info}，{file_path[1]}不是Excel或者Word文件")

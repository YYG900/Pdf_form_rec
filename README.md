# Pdf_form_rec
基于OCR技术的PDF信息表单识别
在工业领域场景下，质检环节至关重要，其中对于信息校验部分，常常需要质检人员一一核对产品的信息，通常质检人员打开待检测PDF文件，对照网页端标准答案，进行核对和黑名单检测。为此，需要开发一个通用的文字识别器与核验器，不需要由用户来框选区域就可以进行自动识别PDF表单中的信息，并将其保存为文本文件，以便于质检人员核验其信息准确性。在诸多文本信息提取方法中，使用OCR来识别PDF中的文字是一种十分高效的方法，但由于实际的应用场景只需要识别出PDF表格中的文字信息，如果识别PDF中的全部文字信息，后期仍需要人工筛选出有用的信息，无法满足自动化的需求。本项目实现了一种基于PPOCR平台的信息表单识别方法，能够有效的识别出PDF中表格所在的区域，并将其重建为Excel文件，能直接用于后续的信息检验与校核。同时本项目开发了配套使用的人机交互软件，提高了该方法的实用性，降低了使用门槛。

使用PPOCR需要先安装PaddlePaddle框架，同时需要安装环境中有相应版本的CUDA与cuDNN，本文采用的方法是包含CUDA与cuDNN的Anaconda中安装PaddlePaddle环境。

    Anaconda下载地址：https://www.anaconda.com/products/distribution#Downloads

安装好Anaconda后，打开Anaconda的终端，在终端中输入如下命令安装PaddlePaddle环境。

    python -m pip install paddlepaddle-gpu==2.2.2 -i https://mirror.baidu.com/pypi/simple

最后下载PPOCR源代码

    PPOCR开源地址：https://github.com/PaddlePaddle/PaddleOCR

本项目基于CUDA10.2的PaddlePaddle环境，在i5-8300H和GTX 1060(6G) MAX-Q机器上进行训练和测试。

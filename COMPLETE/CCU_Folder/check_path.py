import sys, os

def main():
    print(f"현재 파일의 경로={__file__}") 
    print(f"현재 파일의 절대 경로={os.path.abspath(__file__)}")
    print(f"현재 파일의 디렉토리={os.path.dirname(os.path.abspath(__file__))}")
    print(f"현재 파일의 상위 디렉토리={os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")

if __name__ == "__main__":
    main()
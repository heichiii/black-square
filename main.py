import sys
import threading
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from ctypes import windll, c_int

class BlackSquareWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hwnd = None
        self.is_running = True
        self.is_transparent = False  # 跟踪透明状态
        
        # 窗口设置
        self.setWindowTitle("Black Square")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: black;")
        
        # 设置窗口标志：置顶
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # 创建中央部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # label = QLabel("Black Square Window\n\nDrag to resize and move\nCtrl+Q to exit")
        # label.setStyleSheet("color: white; font-size: 14px;")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(label)
        
        # 添加切换按钮
        self.toggle_button = QPushButton("toggle")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 5px;
                padding: 3px;
                font-size: 8px;
            }
            QPushButton:hover {
                background-color: #444;
                border-color: #777;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        self.toggle_button.clicked.connect(self._toggle_transparency)
        layout.addWidget(self.toggle_button)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # 设置为可调整大小
        self.setMouseTracking(True)
        
        # 获取窗口句柄
        self.show()
        self.hwnd = int(self.winId())
        
        # 启动后台线程持续应用置顶效果
        self.timer = QTimer()
        self.timer.timeout.connect(self._ensure_topmost)
        self.timer.start(50)  # 每 50ms 检查一次
    
    def _ensure_topmost(self):
        """确保窗口始终置顶"""
        if not self.hwnd:
            return
        
        try:
            # 强制设置为最前窗口
            windll.user32.SetWindowPos(
                self.hwnd,
                -1,  # HWND_TOPMOST
                0, 0, 0, 0,
                0x0002 | 0x0001 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
            
            # 如果窗口被最小化或隐藏，则显示
            if not windll.user32.IsWindowVisible(self.hwnd):
                windll.user32.ShowWindow(self.hwnd, 5)  # SW_SHOW
        except:
            pass
    
    def _toggle_transparency(self):
        """切换窗口透明度"""
        self.is_transparent = not self.is_transparent
        
        if self.is_transparent:
            # 设置为透明
            self.setWindowOpacity(0.1)
            # self.toggle_button.setText("")
        else:
            # 设置为全黑（不透明）
            self.setWindowOpacity(1.0)
            # self.toggle_button.setText("当前：全黑 (点击切换)")
    
    def keyPressEvent(self, event):
        """快捷键处理"""
        if event.key() == Qt.Key.Key_Q and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """关闭事件"""
        self.timer.stop()
        self.is_running = False
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = BlackSquareWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

def checker_module():
    import sys
    import subprocess

    try:
        # 없는 라이브러리 import시 에러 발생
        import numpy
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'numpy'])
        
    try:
        # 없는 라이브러리 import시 에러 발생
        import scipy
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'scipy'])

    try:
        # 없는 라이브러리 import시 에러 발생
        import pandas
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pandas'])

    try:
        # 없는 라이브러리 import시 에러 발생
        import matplotlib
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'matplotlib'])

    try:
        # 없는 라이브러리 import시 에러 발생
        import pickle
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pickle'])

    try:
        # 없는 라이브러리 import시 에러 발생
        import PyQt5
    except:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', '--upgrade', 'PyQt5'])

    return True


# 라이브러리 설치 여부 체크
if (checker_module()):
    import io
    import os
    import sys
    import time

    import pandas as pd
    import numpy as np

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap, QColor

    import pickle

if not os.path.exists('.\img'):
    os.mkdir('.\img')


if not os.path.exists('.\pickle'):
    os.mkdir('.\pickle')


class DataProcessing:
    def __init__(self):
        # 데이터 로드
        for path in [_ for _ in os.listdir(os.getcwd()+'\\csv') if _.endswith('.csv')]:
            if path.startswith('5대'):
                CRIME_DATA_PATH = os.getcwd() + '\\csv\\' + path
                crime_df = pd.read_csv(CRIME_DATA_PATH)
                crime_df.drop(['자치구별(1)'], axis=1, inplace=True)
                crime_df = crime_df.rename({'자치구별(2)': '자치구'}, axis=1)
                crime_df = crime_df.set_index(
                    '자치구', drop=False)             # 자치구 컬럼 인덱스로 변경
                crime_df.drop(['자치구'], axis=1, inplace=True)
                crime_df.drop(['자치구별(2)'], axis=0, inplace=True)
                crime_df = crime_df.rename({'소계': '서울시'})
                crime_df = crime_df.rename(
                    columns=lambda x: x.replace('.1', ''))
                self.crime_df = crime_df.astype('int')

            else:
                CCTV_DATA_PATH = os.getcwd() + '\\csv\\' + path
                cctv_df = pd.read_csv(CCTV_DATA_PATH, encoding='cp949')
                cctv_df = cctv_df.rename({'구분': '자치구'}, axis=1)
                cctv_df = cctv_df.set_index('자치구', drop=False)
                cctv_df.drop(['자치구'], axis=1, inplace=True)
                cctv_df.drop(['2022년'], axis=1, inplace=True)
                cctv_df = cctv_df.rename(columns=lambda x: x.replace('년', ''))
                # 데이터 int형으로 변환
                for column in cctv_df.columns.tolist():
                    for i in range(len(cctv_df[column])):
                        if type(cctv_df[column][1]) == str:
                            cctv_df[column][i] = cctv_df[column][i].replace(
                                ',', '')
                cctv_df = cctv_df.astype('int')

                # 서울시 총합 데이터 행 추가
                sum_list = []
                for i in range(len(cctv_df.columns)):
                    sum_list.append(sum(cctv_df.iloc[i, :]))
                cctv_df.loc['서울시'] = sum_list
                self.cctv_df = cctv_df


    # 서울시 자치구 목록을 가져오는 함수
    def get_gu_list(self):
        return list(filter(lambda x: x != '서울시', self.crime_df.index.tolist()))


    # 자치구 선택 함수
    def select_gu(self, gu):
        # 선택한 자치구의 연도별 데이터를 반환
        return [self.crime_df.loc[gu], self.cctv_df.loc[gu]]


    # 년도 선택 함수
    def select_year(self, data_list, start_year, end_year):
        selected_data_list = []
        # 선택한 년도의 범죄 데이터를 리스트에 추가
        selected_data_list.append(data_list[0][start_year:end_year])
        # 선택한 년도의 cctv 데이터를 리스트에 추가
        selected_data_list.append(data_list[1][start_year:end_year])
        # 선택한 년도의 인구 데이터를 리스트에 추가
        return selected_data_list


# 저장 리스트의 그래프 정보 및 데이터 데이터 값 그대로 저장
def update_bookmark(pickle_list):
    with open(os.getcwd() + '\\pickle\\pickle.pkl', 'wb') as f:
        pickle.dump(pickle_list, f)


# 저장한 데이터 불러오기
def load_bookmark():
    try:
        with open(os.getcwd() + '\\pickle\\pickle.pkl', 'rb') as f:
            bookmark_list = pickle.load(f)
    except:
        bookmark_list = []
    return bookmark_list


class GuButton(QRadioButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class AddListBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class SaveBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class BtnGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)


class TitleLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class SubTitleLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class HrLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)


class PeriodLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class FooterLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class SaveButton(QGroupBox):
    def __init__(self, text, index, clecked_event, del_event, parent=None):
        super().__init__(parent)
        c_btn = CustomButton(text, index)
        c_btn.clicked.connect(lambda: clecked_event(index))
        c_btn.setFixedSize(80, 36)

        d_btn = DelButton('X')
        d_btn.clicked.connect(lambda: del_event(index))
        d_btn.setFixedSize(30, 36)

        layout = QHBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(c_btn)
        layout.addWidget(d_btn)
        self.setFixedSize(120, 46)
        self.setLayout(layout)


class CustomButton(QPushButton):
    def __init__(self, text, index, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.setToolTip('')
        self.setToolTipDuration(0)

    def enterEvent(self, event):
        self.custom_tooltip = CustomToolTip(self.index, self)
        self.custom_tooltip.show()

    def leaveEvent(self, event):
        self.custom_tooltip.hide()


class DelButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)


class CustomToolTip(QDialog):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        if len(SaveList.get_list()) > 0:
            self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            self.data = SaveList.get_selected_list(index)
            layout = QVBoxLayout()
            layout.setSpacing(0)

            pixmap_label = QLabel()
            pixmap_label.resize(450, 300)
            pixmap_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            # QByteArray 또는 bytes를 QPixmap으로 변환합니다.
            pixmap = QPixmap()
            pixmap.loadFromData(self.data['image'])
            pixmap = pixmap.scaled(pixmap_label.width(), pixmap_label.height())

            if self.data['type'] == 0:
                graph_type = '선형 그래프'
            else:
                graph_type = '막대 그래프'

            graph_info_label = QLabel('{}\n{}~{}\n{}\n{}'.format(
                self.data['gu'], self.data['years'][0], self.data['years'][1], ','.join(self.data['legends']), graph_type))
            graph_info_label.setStyleSheet(
                'background-color: #fff;padding:20px 20px 0 20px;')
            graph_info_label.setFixedWidth(450)

            pixmap_label.setPixmap(pixmap)

            layout.addWidget(graph_info_label)
            layout.addWidget(pixmap_label)

            box = BtnGroup()
            box.setStyleSheet(
                'background-color: #fff')
            box.setLayout(layout)

            box_layout = QVBoxLayout()
            box_layout.addWidget(box)

            self.setLayout(box_layout)

    def showEvent(self, event):
        super().showEvent(event)

    def hideEvent(self, event):
        super().hideEvent(event)


# 데이터 관리
class SaveList:
    instance = None
    global_save_list = load_bookmark()

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    @classmethod
    def get_list(cls):
        return cls.global_save_list

    @classmethod
    def get_selected_list(cls, index):
        if len(cls.global_save_list) > index:
            return cls.global_save_list[index]
        else:
            raise IndexError("Index out of range")

    @classmethod
    def set_list(cls, save_data):
        cls.global_save_list.append(save_data)
        update_bookmark(cls.global_save_list)

    @classmethod
    def del_item(cls, index):
        if len(cls.global_save_list) > index:
            del cls.global_save_list[index]
            update_bookmark(cls.global_save_list)
        else:
            raise IndexError("Index out of range")


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.lode_index = 10
        self.selectde_data = {}
        self.data_p = DataProcessing()
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(self.p)

        self.set_style()
        self.init_ui()

        self.resize(660, 700)
        self.setWindowTitle("CrimeGuard360")
        self.update_plot()
        self.window_position()

    def set_style(self):
        with open("ui_style", 'r') as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        # 각 위젯을 배치할 레이아웃 생성
        main_layout = QVBoxLayout()
        self.visualize_layout = QVBoxLayout()
        self.save_btn_layout = QHBoxLayout()
        title_layout = QVBoxLayout()

        # 타이틀 라벨
        title_label = TitleLabel()
        title_label.setText("Crime Guard 360")
        title_label.setAlignment(Qt.AlignHCenter)
        title_label.setGeometry(0, 0, self.width(), 50)
        title_layout.addWidget(title_label)

        # 서브타이틀 라벨
        subtitle_label = SubTitleLabel()
        subtitle_label.setText("서울시 자치구별 연도별 CCTV 설치 개수에 따른 범죄 예방/검거율")
        subtitle_label.setAlignment(Qt.AlignHCenter)
        subtitle_label.setGeometry(
            0, title_label.height() + 10, self.width(), 50)
        title_layout.addWidget(subtitle_label)

        # 자치구 선택 파트
        groupbox = BtnGroup()  # QGroupBox를 생성
        groupbox.setObjectName('gu_group')

        select_gu_layout = QGridLayout()

        gu_lable = QLabel()
        gu_lable.setText('지역 선택')
        gu_lable.setStyleSheet('font-size:18px;'
                               'font:bold;')
        select_gu_layout.addWidget(gu_lable, 0, 0)

        gu_list = sorted(self.data_p.get_gu_list())
        gu_list.insert(0, '서울시')

        x = 0
        y = 20
        for i in range(len(gu_list)):
            btn = GuButton(gu_list[i])
            btn.clicked.connect(self.update_plot)
            if i == 0:
                btn.setChecked(True)

            btn.setFixedSize(80, 32)

            select_gu_layout.addWidget(btn, y, x)
            x += 10
            if i % 5 == 0:
                y += 10
                x = 0

        groupbox.setLayout(select_gu_layout)

        # 기간 우측 정렬용 레이아웃 생성
        combobox_group = QGroupBox()
        combobox_group.setObjectName('combobox_group')
        combobox_layout = QHBoxLayout()
        combobox_layout.addStretch()
        # 기간

        # label
        combo_title_label = PeriodLabel("기간")
        combo_period_label = PeriodLabel(" ~ ")
        year_list = list(self.data_p.cctv_df.columns)

        for i in range(2):
            combo = QComboBox()
            combo.addItems(year_list)
            # 디폴트로 선택될 연도 설정
            combo.setCurrentIndex(i*6)
            # 콤보박스의 선택 사항이 변경될 때마다 showGraph 메서드를 호출
            combo.currentIndexChanged.connect(self.update_plot)
            if i == 0:
                combobox_layout.addWidget(combo_title_label, 0, Qt.AlignRight)
            else:
                combobox_layout.addWidget(combo_period_label, 0, Qt.AlignRight)
            combobox_layout.addWidget(combo, 0, Qt.AlignRight)

        combobox_group.setLayout(combobox_layout)
       # 체크박스 수정
        checkbox_group = QGroupBox()
        checkbox_group.setObjectName('checkbox_group')
        # 체크박스 우측 정렬용 레이아웃 생성
        checkbox_layout = QHBoxLayout()

        # 우측 정렬용 스팬 추가
        checkbox_layout.addStretch()

        for name in ['범죄 발생 건수', '범죄 검거 건수', 'CCTV 설치수']:
            checkbox = QCheckBox(name)
            checkbox.setChecked(True)
            checkbox.setObjectName(name)
            checkbox.clicked.connect(self.update_plot)
            checkbox_layout.addWidget(checkbox, 0, Qt.AlignRight)

        checkbox_group.setLayout(checkbox_layout)

        graph_bottom_box = QGroupBox()  # QGroupBox를 생성
        graph_bottom_box.setObjectName('graph_group')

        graph_bottom_layout = QHBoxLayout()

        line_graph_btn = QRadioButton('선형 그래프')
        line_graph_btn.clicked.connect(self.update_plot)
        line_graph_btn.setChecked(True)

        bar_graph_btn = QRadioButton('막대 그래프')
        bar_graph_btn.clicked.connect(self.update_plot)

        graph_bottom_layout.addWidget(line_graph_btn)
        graph_bottom_layout.addWidget(bar_graph_btn)

        graph_bottom_layout.addStretch()
        add_btn = AddListBtn('저장리스트에 추가')
        add_btn.clicked.connect(self.add_current_data)
        graph_bottom_layout.addWidget(add_btn, 0, Qt.AlignRight)
        graph_bottom_box.setLayout(graph_bottom_layout)

        save_btn_group = BtnGroup()

        h_layout = QHBoxLayout()
        self.save_btn_layout.setAlignment(Qt.AlignLeft)

        save_list_label = QLabel('저장 리스트 |')
        save_list_label.setStyleSheet("color:gray;font-size:12px;")
        save_list_label.setFixedSize(80, 46)

        save_btn = SaveBtn('저장')
        save_btn.clicked.connect(self.save_img)
        save_btn.setFixedSize(80, 36)

        h_layout.addWidget(save_list_label)
        h_layout.setAlignment(save_list_label, Qt.AlignLeft)
        h_layout.addLayout(self.save_btn_layout)
        h_layout.addWidget(save_btn)
        h_layout.setAlignment(save_btn, Qt.AlignRight)

        save_btn_group.setLayout(h_layout)

        footer_layout = QVBoxLayout()

        footer_label1 = FooterLabel('     *최대 3개까지 저장 가능합니다.\n')
        footer_label2 = FooterLabel()
        footer_label2.setText(
            "이 프로젝트는 다양한 외부요인이 일정한 상수로 유지되는 가정하에 진행된 프로젝트입니다.\n해당 결과는 cctv 개수와 범죄 발생 및 검거를 비교하기 위한 방식이며,\n외부 요인을 고려하지 않은 가정 하에 유의미합니다.")
        footer_label2.setAlignment(Qt.AlignCenter)

        footer_layout.addWidget(footer_label1)
        footer_layout.setAlignment(footer_label1, Qt.AlignLeft)
        footer_layout.addWidget(footer_label2)
        footer_layout.setAlignment(footer_label2, Qt.AlignHCenter)

        # 스크롤 영역 위젯 생성
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        # 상하 스크롤 안보이게 설정
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        layout = QVBoxLayout()

        layout.addLayout(title_layout)
        layout.addWidget(HrLabel())
        layout.addWidget(groupbox)
        layout.addWidget(combobox_group)
        layout.addWidget(checkbox_group)
        layout.addWidget(HrLabel())
        layout.addLayout(self.visualize_layout)
        layout.addWidget(HrLabel())
        layout.addWidget(graph_bottom_box)
        layout.addWidget(save_btn_group)
        layout.addLayout(footer_layout)

        self.create_save_btn()

        scroll_widget.setLayout(layout)
        scroll_widget.setPalette(self.p)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.show()

    def window_position(self):
        # 현재 모니터의 크기 구하기
        screen = QDesktopWidget().screenGeometry()

        # UI 창의 크기 가져오기
        size = self.geometry()

        # UI 창 중앙 위치 계산하기
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2

        # UI 창 위치 조정하기
        self.move(x, y)


    def update_plot(self):
        legend_list = []
        years = []

        # 레이아웃 초기화
        while self.visualize_layout.count():
            child = self.visualize_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 세팅값을 가져오는지 새로 만든것인지 구분
        if (self.lode_index != 10):
            # 저장 리스트의 버튼을 누를시 저장된 데이터를 적용
            data = SaveList.get_selected_list(self.lode_index)
            gu = data['gu']
            years = data['years']
            legend_list = data['legends']
            graph_type = data['type']
            self.lode_index = 10

        else:
            gu = list(filter(lambda x: x.isChecked(), self.findChild(
                QGroupBox, 'gu_group').children()[2:]))[0].text()

            selected_year = self.findChild(
                QGroupBox, 'combobox_group').children()[2::2]
            
            start_year = int(selected_year[0].currentIndex())
            end_year = int(selected_year[1].currentIndex())

            if end_year-start_year < 0:
                selected_year[0].setCurrentIndex(end_year)


            for item in selected_year:
                years.append(item.currentText()[:4])

            legend = list(filter(lambda x: x.isChecked(), self.findChild(
                QGroupBox, 'checkbox_group').children()[1:]))

            for item in legend:
                legend_list.append(item.text())

            # -1일시 bar 그래프
            graph_type = list(filter(lambda x: x.isChecked(), self.findChild(
                QGroupBox, 'graph_group').children()[1:3]))[0].text().find('선형')

        # 선택한 자치구의 범죄 데이터와 cctv데이터를 데이터 프레임에 저장
        gu_crime_df, gu_cctv_df = self.data_p.select_gu(gu)

        gu_crime_df, gu_cctv_df = self.data_p.select_year(
            [gu_crime_df, gu_cctv_df], years[0], years[1])

        year = list(gu_cctv_df.index)  # 년도 리스트

        # cctv데이터와 범죄 발생 데이터의 상관계수
        correlation = np.corrcoef(gu_cctv_df, gu_crime_df[0::2])

        arest_rate = 0
        for i in range(len(year)):
            arest_rate += (gu_crime_df[i*2+1]/gu_crime_df[i*2]) * 100

        # 예방율 계산
        prvnt_rate = round((1 - correlation[0,1]**2) * 100,2)

        # 검거율 계산
        arest_rate = round(arest_rate/len(year),2)

        # 그래프를 그릴 Figure 생성
        plt.rc('font', family='Malgun Gothic')
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # 그래프 그리기
        ax = self.fig.add_subplot(111)
        ax.set_title(gu)

        # 막대그래프 간격 조절
        x = np.arange(len(year))
        width = 0.2
        x_bar = [[x], [x-width/2, x+width/2], [x-width, x, x+width]]

        # 범례와 그래프 종류에 따라 그래프 를 그리는 기능
        for i in range(len(legend_list)):
            if legend_list[i] == '범죄 발생 건수':
                if graph_type == -1:
                    ax.bar(x_bar[len(legend_list)-1][i],
                            gu_crime_df[0::2], width, label="발생")
                else:
                    ax.plot(gu_crime_df[0::2], 'o-', label="발생")

                self.findChild(QGroupBox, 'checkbox_group').children()[
                    1].setChecked(True)

            elif legend_list[i] == '범죄 검거 건수':
                if graph_type == -1:
                    ax.bar(x_bar[len(legend_list)-1][i],
                            gu_crime_df[1::2], width, label="검거")
                else:
                    ax.plot(gu_crime_df[1::2], 'o-', label="검거")

                self.findChild(QGroupBox, 'checkbox_group').children()[
                    2].setChecked(True)

            else:
                if graph_type == -1:
                    ax.bar(x_bar[len(legend_list)-1][i],
                            gu_cctv_df, width, label="cctv")
                else:
                    ax.plot(gu_cctv_df, 'o-', label="cctv")

                self.findChild(QGroupBox, 'checkbox_group').children()[
                    3].setChecked(True)

        for item in self.findChild(QGroupBox, 'checkbox_group').children()[1:]:
            item.setChecked(False)
            for check in legend_list:
                if check == item.text():
                    item.setChecked(True)

        ax.set_xticks(x)
        ax.set_xticklabels(year)
        ax.legend()
        self.canvas.draw()

        p_label = QLabel()
        p_label.setStyleSheet('font-size:16px;font:500;')
        p_label.setText("예방율 : {}%\t\n검거율 : {}%\t".format(prvnt_rate,arest_rate))

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(p_label)
        layout.setAlignment(p_label, Qt.AlignRight)
        

        label = QLabel()
        label.setFixedHeight(400)
        label.setLayout(layout)

        # 레이아웃 초기화
        while self.visualize_layout.count():
            child = self.visualize_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.visualize_layout.addWidget(label)

        # 그래프 이미지로 저장
        buffer = io.BytesIO()
        self.fig.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        image = buffer.getvalue()

        # 현재 선택된 데이터 변수로 관리
        self.selectde_data = {
            'gu': gu,  # str
            'years': years,  # [str,str]
            'legends': legend_list,  # [str 0~3]
            'type': graph_type,  # int
            'image': image
        }


    # 저장리스트에 데이터 저장
    def add_current_data(self):
        if len(SaveList.get_list()) > 2:
            QMessageBox.information(
                self, 'error', '최대 저장 개수 3개를 초과하여 저장할 수 없습니다.')
        else:
            SaveList.set_list(self.selectde_data)
            self.create_save_btn()


    # 저장된 셋팅값 불러오기
    def save_data_load(self, index):
        self.lode_index = index
        self.update_plot()


    # 저장리스트 데이터 삭제
    def delete_save_btn(self, index):
        SaveList.del_item(index)
        self.create_save_btn()


    # 저장된 이미지를 파일로 저장
    def save_img(self):
        li = SaveList.get_list()
        if len(li) == 0:
            QMessageBox.information(
                self, 'error', '저장 리스트에 데이터가 없습니다.')
        else:
            current_time = time.strftime('%m-%d %H.%M.%S')
            for i in range(len(li)):
                with open(os.getcwd() + '\\img\\' + current_time +"_0" + str(i+1) + '.' + li[i]['gu']+'.png', 'wb') as f:
                    f.write(li[i]['image'])


    # 저장리스트에 값만큼 동적으로 버튼을 생성
    def create_save_btn(self):
        while self.save_btn_layout.count():
            child = self.save_btn_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for index in range(len(SaveList.get_list())):
            text = "0" + str(index+1) + "." + \
                SaveList.get_selected_list(index)['gu']
            btn = SaveButton(text, index, self.save_data_load,
                             self.delete_save_btn)
            self.save_btn_layout.addWidget(btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

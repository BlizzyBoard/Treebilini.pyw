import sys
import random
import subprocess
import datetime
import webbrowser
import os
import urllib.parse
import shutil
from send2trash import send2trash
import platform 

from plyer import notification 

from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMenu, QSystemTrayIcon, QMessageBox, QInputDialog, QStyle, QComboBox, QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit

from PySide6.QtGui import (
    QMovie, QMouseEvent, QIcon, QPixmap, QAction,
    QContextMenuEvent, QVector2D,
    QDragEnterEvent, QDragMoveEvent, QDropEvent, QCursor
)
from PySide6.QtCore import Qt, QPoint, QTimer, QCoreApplication, QPropertyAnimation, QSize, QRect

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! REEMPLAZA 'USUARIO' CON TU NOMBRE DE USUARIO REAL.
# Ejemplo: r"C:\Users\TuNombreDeUsuario\Pictures\animations"
BASE_ANIMATION_PATH = r"C:\Users\USUARIO\Pictures\animations" 

NORMAL_IMAGE_PATH = os.path.join(BASE_ANIMATION_PATH, "Normal.png")
GIF_IDLE_PATH = os.path.join(BASE_ANIMATION_PATH, "pixil-gif-drawing.gif")
GIF_TALK_PATH = os.path.join(BASE_ANIMATION_PATH, "talking.gif")
ICON_PATH = os.path.join(BASE_ANIMATION_PATH, "Icono.ico") # ASEGÚRATE QUE SEA .ico

GIF_ROBBING_PATH = os.path.join(BASE_ANIMATION_PATH, "robbing.gif")
GIF_STEALING_LEFT_UP_PATH = os.path.join(BASE_ANIMATION_PATH, "stealingleftup.gif")
GIF_STEALING_RIGHT_PATH = os.path.join(BASE_ANIMATION_PATH, "stealingright.gif")
IMG_STEALING_DOWN_PATH = os.path.join(BASE_ANIMATION_PATH, "Stealing.png")
GIF_DELETE_PATH = os.path.join(BASE_ANIMATION_PATH, "delete.gif")
GIF_STEALING_FAIL_PATH = os.path.join(BASE_ANIMATION_PATH, "Stealingfail.gif")

GIF_WALK_HORIZONTAL_PATH = os.path.join(BASE_ANIMATION_PATH, "pixil-gif-drawing.gif")
GIF_UPPING_PATH = os.path.join(BASE_ANIMATION_PATH, "upping.gif")
GIF_UPPING_LEFT_PATH = os.path.join(BASE_ANIMATION_PATH, "uppingleft.gif")
GIF_UPPING_RIGHT_PATH = os.path.join(BASE_ANIMATION_PATH, "uppingright.gif")

CHARACTER_SIZE = QSize(128, 128)

MOVEMENT_DURATION_MIN_MS = 3000
MOVEMENT_DURATION_MAX_MS = 8000

TALK_ANIMATION_DURATION_MS = 2000
IDLE_DURATION_MS_MIN = 1000
IDLE_DURATION_MS_MAX = 4000
NORMAL_STATE_DURATION_MS_MIN = 1000
NORMAL_STATE_DURATION_MS_MAX = 3000

EVENT_ANIMATION_KEY = "walk_horizontal"
EVENT_ANIMATION_DURATION_MS = 1500
EVENT_TRIGGER_DELAY_MIN_MS = 5000
EVENT_TRIGGER_DELAY_MAX = 15000

ROBBING_DURATION_MS = 15000

RECYCLE_COMPLETED_ROBBERY_TARGET_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Papelera de reciclaje")

ROB_INITIATION_DELAY_MIN_MS = 50
ROB_INITIATION_DELAY_MAX_MS = 200
ROB_COOLDOWN_MIN_MS = 10000
ROB_COOLDOWN_MAX_MS = 20000

ESCAPE_SPEED_PPS = 250

DROP_ANIMATION_DURATION_MS = 1500
DELETE_ANIMATION_DURATION_MS = 1500

STRESS_DURATION_MS = 10000 
STRESS_MOVEMENT_SPEED_PPS = 400 
STRESS_ANIMATION_PATH = os.path.join(BASE_ANIMATION_PATH, "stressed.gif") 

# --- NEW ADWARE CONFIGURATION ---
RANDOM_AD_DELAY_MIN_MS = 30000 
RANDOM_AD_DELAY_MAX_MS = 120000 
MOVISTAR_AD_CHANCE = 0.05 
MOVISTAR_AD_IMAGE_PATH = os.path.join(BASE_ANIMATION_PATH, "pop-up.png") 

GENERIC_ADS = [
    ("¡Tu PC está lento!", "Haz clic aquí para optimizarlo."),
    ("¿Quieres ganar un iPhone 15?", "¡Haz clic y participa!"),
    ("Oferta imperdible:", "¡Antivirus gratis por 30 días!"),
    ("Tu cuenta de correo en riesgo", "Verifica ahora."),
    ("¡Felicidades, ganador!", "Eres el visitante 1.000.000. Reclama tu premio."),
    ("Gana dinero fácil", "Descubre cómo ganar dinero desde casa."),
    ("¡Alerta de virus!", "Detectamos 14 virus en tu sistema."),
    ("Juega ahora mismo", "El mejor juego online te espera, ¡juega gratis!"),
    ("Vuelos baratos te esperan", "¿Buscas vuelos? ¡Encuentra las mejores ofertas!"),
    ("Ahorra en tu factura", "¡Ahorra en tu factura de luz! Descubre nuestro secreto.")
]
# --- END NEW ADWARE CONFIGURATION ---

ANTIVIRUS_INFO = {
    "Microsoft Defender": {
        "url": "https://www.microsoft.com/es-es/windows/comprehensive-security",
        "installed": True,
        "scan_command": "powershell.exe -Command \"Start-MpScan -ScanType QuickScan\"",
        "scan_guide": "Para iniciar un análisis rápido de Windows Defender, abre 'Seguridad de Windows' > 'Protección contra virus y amenazas' > 'Opciones de examen' y selecciona 'Examen rápido'."
    },
    "Malwarebytes": {
        "url": "https://www.malwarebytes.com/mwb-download",
        "installed": True, 
        "scan_command": None, 
        "scan_guide": "Para iniciar un análisis en Malwarebytes, abre la aplicación, ve a la sección 'Escáner' o 'Analizar' y busca la opción de 'Análisis de amenazas' o 'Análisis personalizado'."
    },
    "Avast Free Antivirus": {
        "url": "https://www.avast.com/es-es/free-antivirus-download",
        "installed": False, 
        "scan_command": None,
        "scan_guide": "Para iniciar un análisis en Avast, abre la aplicación, ve a 'Protección' > 'Análisis de virus' y selecciona el tipo de análisis (ej. 'Análisis inteligente' o 'Análisis completo')."
    },
    "AVG AntiVirus Free": {
        "url": "https://www.avg.com/es-es/download-antivirus",
        "installed": False,
        "scan_command": None,
        "scan_guide": "Para iniciar un análisis en AVG, abre la aplicación, haz clic en 'Análisis' o 'Escanear ahora' en la pantalla principal."
    },
    "Kaspersky Security Cloud Free": {
        "url": "https://www.kaspersky.es/free-cloud-security",
        "installed": False,
        "scan_command": None,
        "scan_guide": "Para iniciar un análisis en Kaspersky, abre la aplicación, ve a la sección 'Análisis' y elige el tipo de análisis que desees."
    }
}

class AntivirusSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Antivirus para Analizar PC")
        self.setFixedSize(350, 150) 

        self.layout = QVBoxLayout()
        
        self.label = QLabel("¿Con qué antivirus quieres ejecutar esto?")
        self.layout.addWidget(self.label)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(ANTIVIRUS_INFO.keys())
        self.layout.addWidget(self.combo_box)
        
        self.buttons_layout = QHBoxLayout()
        self.select_button = QPushButton("Seleccionar", self)
        self.select_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.select_button)

        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)
        
        self.setLayout(self.layout)
        self.selected_antivirus = None
        
    def accept(self):
        self.selected_antivirus = self.combo_box.currentText()
        super().accept()


class Treebilini(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)

        self.setGeometry(0, 0, CHARACTER_SIZE.width(), CHARACTER_SIZE.height())

        self.animations = {
            "normal": NORMAL_IMAGE_PATH,
            "idle": GIF_IDLE_PATH,
            "talk": GIF_TALK_PATH,
            "walk_horizontal": GIF_WALK_HORIZONTAL_PATH,
            "upping": GIF_UPPING_PATH,
            "upping_left": GIF_UPPING_LEFT_PATH,
            "upping_right": GIF_UPPING_RIGHT_PATH,
            "robbing": GIF_ROBBING_PATH,
            "stealing_left_up": GIF_STEALING_LEFT_UP_PATH,
            "stealing_right": GIF_STEALING_RIGHT_PATH,
            "stealing_down": IMG_STEALING_DOWN_PATH,
            "delete": GIF_DELETE_PATH,
            "stealing_fail": GIF_STEALING_FAIL_PATH,
            "stressed": STRESS_ANIMATION_PATH, 
        }
        self.current_animation_state = "normal"

        self.direction_to_animation = {
            (0, -1): "upping",
            (-1, -1): "upping_left",
            (1, -1): "upping_right",
            (1, 0): "walk_horizontal",
            (-1, 0): "walk_horizontal",
            (0, 1): "normal",
            (-1, 1): "normal",
            (1, 1): "normal",
        }
        
        self.stressed_direction_to_animation = {
            (0, -1): "upping",
            (-1, -1): "upping_left",
            (1, -1): "upping_right",
            (1, 0): "walk_horizontal",
            (-1, 0): "walk_horizontal",
            (0, 1): "walk_horizontal",
            (-1, 1): "walk_horizontal",
            (1, 1): "walk_horizontal",
        }


        self.robbing_direction_to_animation = {
            (-1, -1): "stealing_left_up",
            (1, -1): "stealing_right",
            (0, -1): "stealing_right",
            (0, 1): "stealing_down",
            (-1, 1): "stealing_down",
            (1, 1): "stealing_down",
            (1, 0): "stealing_right",
            (-1, 0): "stealing_left_up",
        }

        self.movie = QMovie()
        self.pixmap = QPixmap()
        self.movie_label = QLabel(self)
        self.movie_label.setFixedSize(CHARACTER_SIZE.width(), CHARACTER_SIZE.height())

        self._set_animation("normal")

        self.old_pos = QPoint()

        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.finished.connect(self._movement_finished)

        self.normal_state_timer = QTimer(self)
        self.normal_state_timer.timeout.connect(self._start_new_movement)

        self.random_event_animation_timer = QTimer(self)
        self.random_event_animation_timer.timeout.connect(self._trigger_random_event_animation)

        self.robbery_timer = QTimer(self)
        self.robbery_timer.setSingleShot(True)
        self.robbery_timer.timeout.connect(self._handle_timed_robbery)

        self.rob_initiation_timer = QTimer(self)
        self.rob_initiation_timer.setSingleShot(True)
        self.rob_initiation_timer.timeout.connect(self._initiate_robbery_attempt)

        self.rob_cooldown_timer = QTimer(self)
        self.rob_cooldown_timer.setSingleShot(True)
        self.rob_cooldown_timer.timeout.connect(self._end_rob_cooldown)
        
        self.stress_timer = QTimer(self)
        self.stress_timer.setSingleShot(True)
        self.stress_timer.timeout.connect(self._end_stress_state)

        self.ad_timer = QTimer(self) # <-- Aquí se crea el temporizador para anuncios
        self.ad_timer.setSingleShot(True)
        self.ad_timer.timeout.connect(self._show_random_ad)

        self.is_moving = False
        self.is_event_animating = False
        self.is_talking = False
        self.is_robbing = False
        self.can_rob_again = True
        self.stolen_folder_path = None
        self.folder_awaiting_robbery = None
        self.robbery_start_pos = QPoint()
        self.is_stressed = False

        self._start_normal_state_timer()
        self._start_random_event_timer()
        self._start_ad_timer() # <-- Aquí se inicia por primera vez

        self._setup_tray_icon()

    def _set_animation(self, state: str):
        if not isinstance(state, str) or self.current_animation_state == state:
            return

        path = self.animations.get(state)

        if not path or not os.path.exists(path):
            path = self.animations.get("normal")
            if path is None or not os.path.exists(path):
                return

        if path.lower().endswith(".gif"):
            if self.movie.fileName() != path or self.movie.state() != QMovie.MovieState.Running:
                self.movie.setFileName(path)
                self.movie_label.setMovie(self.movie)
                self.movie.start()
        elif path.lower().endswith((".png", ".jpg", ".jpeg")):
            self.movie.stop()
            self.movie_label.setMovie(None)
            self.pixmap.load(path)
            scaled_pixmap = self.pixmap.scaled(CHARACTER_SIZE.width(), CHARACTER_SIZE.height(),
                                               Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.movie_label.setPixmap(scaled_pixmap)
        else:
            if self.current_animation_state != "normal":
                self._set_animation("normal")

        self.current_animation_state = state

    def _setup_tray_icon(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            icon_to_set = None

            if os.path.exists(ICON_PATH):
                icon_to_set = QIcon(ICON_PATH)
            else:
                if QIcon.hasThemeIcon("system-tray"):
                    icon_to_set = QIcon.fromTheme("system-tray")
                else:
                    icon_to_set = self.style().standardIcon(QStyle.SP_DialogOkButton)

            if icon_to_set:
                self.tray_icon.setIcon(icon_to_set)
            else:
                self.tray_icon.setIcon(QIcon())

            self.tray_icon.setToolTip("Mi Treebilini")

            tray_menu = QMenu()
            exit_action = QAction("Salir", self)
            exit_action.triggered.connect(self.close_application)
            tray_menu.addAction(exit_action)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
        else:
            pass

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_robbing:
                self._handle_dropped_robbery()
            elif self.is_stressed: 
                self._end_stress_state()
            else:
                self.old_pos = event.globalPosition().toPoint()
                self._stop_all_activities()
                self._set_animation("walk_horizontal")

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.is_robbing and not self.is_stressed: 
            self.old_pos = QPoint()
            self._start_normal_state_timer()
            self._start_random_event_timer()
            self._start_ad_timer() 

    def contextMenuEvent(self, event: QContextMenuEvent):
        self._show_context_menu(event.globalPos())

    def _show_context_menu(self, pos: QPoint):
        context_menu = QMenu(self)

        action_calc = QAction("Abrir Calculadora", self)
        action_calc.triggered.connect(self._open_calculator_and_react)
        context_menu.addAction(action_calc)

        action_current_datetime = QAction("Fecha Actual", self)
        action_current_datetime.triggered.connect(lambda: self._trigger_talk_animation_and_action(self._show_full_datetime))
        context_menu.addAction(action_current_datetime)

        action_web_search = QAction("Buscar en Internet", self)
        action_web_search.triggered.connect(lambda: self._trigger_talk_animation_and_action(self._prompt_for_search))
        context_menu.addAction(action_web_search)
        
        action_analyze_pc = QAction("Analizar PC", self)
        action_analyze_pc.triggered.connect(lambda: self._trigger_talk_animation_and_action(self._prompt_for_antivirus_scan))
        context_menu.addAction(action_analyze_pc)

        action_stress = QAction("Estresar a Treebilini", self)
        action_stress.triggered.connect(self._start_stress_state) 
        context_menu.addAction(action_stress)

        action_show_ad = QAction("Mostrar Anuncio", self)
        action_show_ad.triggered.connect(self._show_random_ad)
        context_menu.addAction(action_show_ad)

        context_menu.addSeparator()

        exit_action_direct = QAction("Salir", self)
        exit_action_direct.triggered.connect(self.close_application)
        context_menu.addAction(exit_action_direct)

        context_menu.exec(pos)

    def _trigger_talk_animation_and_action(self, action_func):
        self._stop_all_activities()
        self.is_talking = True

        self._set_animation("talk")
        QTimer.singleShot(TALK_ANIMATION_DURATION_MS, lambda: self._return_to_normal_state_and_action(action_func))

    def _return_to_normal_state_and_action(self, action_func):
        action_func()
        self.is_talking = False

    def _open_calculator_and_react(self):
        try:
            subprocess.Popen(['calc.exe'])
            self._stop_all_activities()
            self.is_talking = True
            self._set_animation("talk")
            QTimer.singleShot(TALK_ANIMATION_DURATION_MS, self._return_to_normal_state_after_action)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir la calculadora.")
            self._return_to_normal_state_after_action()

    def _return_to_normal_state_after_action(self):
        self.is_talking = False
        self._set_animation("normal")
        self._start_normal_state_timer()
        self._start_random_event_timer()
        self._start_ad_timer() 

    def _show_full_datetime(self):
        now = datetime.datetime.now()
        days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        day_of_week = days_of_week[now.weekday()]
        day_number = now.day
        month_name = months[now.month - 1]
        year = now.year

        full_date_str = f"Hoy es {day_of_week}, {day_number} de {month_name} de {year}."
        QMessageBox.information(self, "Fecha Actual", full_date_str)
        self._return_to_normal_state_after_action()


    def _prompt_for_search(self):
        search_text, ok = QInputDialog.getText(self, "Buscar en Internet", "¿Qué quieres buscar en internet?")
        
        if ok and search_text:
            self._perform_web_search(search_text)
        else:
            self._return_to_normal_state_after_action()

    def _perform_web_search(self, query: str):
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        try:
            webbrowser.open(search_url)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el navegador para buscar.")
        self._return_to_normal_state_after_action() 


    def _prompt_for_antivirus_scan(self):
        dialog = AntivirusSelectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            selected_antivirus = dialog.selected_antivirus
            self._perform_antivirus_scan(selected_antivirus)
        else:
            self._return_to_normal_state_after_action()

    def _perform_antivirus_scan(self, antivirus_name: str):
        antivirus_data = ANTIVIRUS_INFO.get(antivirus_name)
        
        if not antivirus_data:
            QMessageBox.warning(self, "Error", f"Antivirus '{antivirus_name}' no reconocido.")
            self._return_to_normal_state_after_action()
            return

        if platform.system() == "Windows" and antivirus_name == "Microsoft Defender":
            if antivirus_data["installed"] and antivirus_data["scan_command"]:
                try:
                    subprocess.Popen(antivirus_data["scan_command"], shell=True)
                    QMessageBox.information(self, "Análisis de PC", 
                                            f"Iniciando análisis rápido de {antivirus_name}. "
                                            f"Se abrirá una ventana de PowerShell/CMD si es necesario.")
                except Exception as e:
                    QMessageBox.warning(self, "Error de Ejecución", 
                                        f"No se pudo iniciar el análisis de {antivirus_name}. "
                                        f"Asegúrate de tener los permisos necesarios. Error: {e}")
            else:
                QMessageBox.warning(self, "Error", 
                                    f"No se encontró un comando de escaneo para {antivirus_name} o no está disponible.")
        else: 
            if antivirus_data["installed"]:
                QMessageBox.information(self, "Análisis de PC", 
                                        f"Para iniciar un análisis real con {antivirus_name}, "
                                        f"sigue estos pasos:\n\n{antivirus_data['scan_guide']}\n\n"
                                        f"Ahora intentaré abrir la aplicación para que puedas hacerlo manualmente.")
                try:
                    subprocess.Popen([antivirus_name]) 
                except FileNotFoundError:
                     QMessageBox.warning(self, "Error al Abrir", 
                                        f"No se pudo abrir la aplicación {antivirus_name} directamente. "
                                        f"Por favor, ábrela manualmente.")
                except Exception as e:
                    QMessageBox.warning(self, "Error al Abrir", 
                                        f"Ocurrió un error al intentar abrir {antivirus_name}: {e}")

            else: 
                reply = QMessageBox.question(self, "Antivirus no encontrado", 
                                             f"No tienes {antivirus_name} instalado. ¿Quieres descargarlo?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        webbrowser.open(antivirus_data["url"])
                        QMessageBox.information(self, "Descarga Iniciada", f"Abriendo el navegador para descargar {antivirus_name}.")
                    except Exception as e:
                        QMessageBox.warning(self, "Error de Descarga", f"No se pudo abrir el navegador para descargar {antivirus_name}.")
        
        self._return_to_normal_state_after_action()


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if self.is_robbing or not self.can_rob_again or self.is_stressed: 
            event.ignore()
            if self.is_robbing:
                QMessageBox.information(self, "Robo de Carpeta", "Treebilini ya está robando o en cooldown. Espera.")
            elif self.is_stressed:
                QMessageBox.information(self, "Treebilini Ocupado", "Treebilini está estresado ahora mismo y no puede robar.")
            return

        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.isdir(file_path):
                self._prepare_for_robbery(file_path)
                event.acceptProposedAction()
            else:
                QMessageBox.information(self, "Robo de Carpeta", "Solo puedo robar carpetas, no archivos.")
                event.ignore()
        else:
            event.ignore()

    def _prepare_for_robbery(self, folder_path: str):
        if self.folder_awaiting_robbery:
            QMessageBox.information(self, "Robo de Carpeta", "Ya tengo una carpeta pendiente de robo. Completa o descarta la anterior.")
            return

        self.folder_awaiting_robbery = folder_path
        self._start_rob_initiation_timer()

    def _start_rob_initiation_timer(self):
        if self.rob_initiation_timer.isActive():
            self.rob_initiation_timer.stop()
        
        if self.folder_awaiting_robbery and self.can_rob_again and not self.is_robbing and not self.is_stressed: 
            delay = random.randint(ROB_INITIATION_DELAY_MIN_MS, ROB_INITIATION_DELAY_MAX_MS)
            self.rob_initiation_timer.start(delay)
        else:
            self._return_to_normal_state_after_robbery()

    def _initiate_robbery_attempt(self):
        if self.folder_awaiting_robbery and self.can_rob_again and not self.is_robbing and not self.is_stressed: 
            self._stop_all_activities()
            self.is_robbing = True
            self.stolen_folder_path = self.folder_awaiting_robbery
            self.folder_awaiting_robbery = None
            self.robbery_start_pos = self.pos()

            self._set_animation("robbing")
            
            QTimer.singleShot(1000, self._start_escape_movement)
            QMessageBox.information(self, "¡Robo en Proceso!",
                                f"¡Treebilini está robando la carpeta '{os.path.basename(self.stolen_folder_path)}'!\n"
                                f"Haz clic en él para detenerlo antes de {ROBBING_DURATION_MS / 1000} segundos.")
            self.robbery_timer.start(ROBBING_DURATION_MS)

        else:
            self._return_to_normal_state_after_robbery()

    def _handle_dropped_robbery(self):
        if not self.is_robbing:
            return
        
        self._stop_robbery_process()
        self._set_animation("stealing_fail")

        QTimer.singleShot(DROP_ANIMATION_DURATION_MS,
                          lambda: self._finalize_dropped_robbery(self.stolen_folder_path or ""))

    def _finalize_dropped_robbery(self, original_stolen_path: str):
        if not original_stolen_path or not os.path.exists(original_stolen_path):
            QMessageBox.warning(self, "Robo Interrumpido", "No se encontró la carpeta original para replicarla o ya no existe.")
            self._return_to_normal_state_after_robbery()
            return

        try:
            target_base_path = os.path.join(os.path.expanduser("~"), "Desktop", "Robo Fallido Treebilini")
            os.makedirs(target_base_path, exist_ok=True)

            folder_name = f"robo_fallido_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            destination_path = os.path.join(target_base_path, folder_name)

            shutil.copytree(original_stolen_path, destination_path)

            QMessageBox.information(self, "Robo Interrumpido",
                                    f"¡Treebilini soltó la carpeta!\n"
                                    f"Se creó una copia de la carpeta robada llamada '{folder_name}' en:\n"
                                    f"{destination_path}")

        except Exception as e:
            QMessageBox.warning(self, "Error al Crear Carpeta", f"No se pudo crear la carpeta 'robo fallido' o copiar su contenido.")

        self._return_to_normal_state_after_robbery()

    def _handle_timed_robbery(self):
        if not self.is_robbing:
            return

        self._stop_robbery_process()

        recycle_bin_rect = self._find_desktop_icon_position("Papelera de reciclaje")

        target_pos = self._get_random_screen_point()
        if recycle_bin_rect:
            icon_center_x = recycle_bin_rect.x() + recycle_bin_rect.width() // 2
            icon_center_y = recycle_bin_rect.y() + recycle_bin_rect.height() // 2
            target_pos = QPoint(icon_center_x - CHARACTER_SIZE.width() // 2,
                                icon_center_y - CHARACTER_SIZE.height() // 2)
        
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(target_pos)

        distance = QVector2D(target_pos - self.pos()).length()
        duration = int(distance / ESCAPE_SPEED_PPS * 1000)
        self.animation.setDuration(max(1000, duration))

        try:
            self.animation.finished.disconnect(self._movement_finished)
        except TypeError:
            pass
        self.animation.finished.connect(self._reached_recycle_bin_destination)

        self._set_animation("delete")
        self.animation.start()

    def _reached_recycle_bin_destination(self):
        self.animation.finished.disconnect(self._reached_recycle_bin_destination)
        self.animation.finished.connect(self._movement_finished)
        self.is_moving = False

        self._set_animation("delete")

        QTimer.singleShot(DELETE_ANIMATION_DURATION_MS, self._finalize_timed_robbery)

    def _finalize_timed_robbery(self):
        if self.stolen_folder_path and os.path.exists(self.stolen_folder_path):
            try:
                send2trash(self.stolen_folder_path)
                QMessageBox.information(self, "Robo Exitoso", f"¡Treebilini se deshizo de la carpeta '{os.path.basename(self.stolen_folder_path)}' en la papelera de reciclaje del sistema!")
            except Exception as e:
                QMessageBox.warning(self, "Error de Papelera", f"No se pudo enviar la carpeta a la papelera del sistema.")
        else:
            pass

        try:
            os.makedirs(RECYCLE_COMPLETED_ROBBERY_TARGET_PATH, exist_ok=True)
            
            completed_folder_name = f"robo_completado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            final_target_path = os.path.join(RECYCLE_COMPLETED_ROBBERY_TARGET_PATH, completed_folder_name)
            os.makedirs(final_target_path, exist_ok=True)

            QMessageBox.information(self, "Robo Completado",
                                    f"Se creó una carpeta vacía '{completed_folder_name}' simulando la finalización del robo en:\n"
                                    f"{RECYCLE_COMPLETED_ROBBERY_TARGET_PATH}")
        except Exception as e:
            QMessageBox.warning(self, "Error de Carpeta", f"No se pudo crear la carpeta 'robo completado'.")

        self._return_to_normal_state_after_robbery()

    def _find_desktop_icon_position(self, folder_name: str):
        target_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)
        if os.path.isdir(target_folder_path):
            desktop = QApplication.primaryScreen().geometry()
            x = desktop.left() + 20
            y = desktop.top() + 20
            return QRect(x, y, 64, 64) 
        return None

    def _stop_robbery_process(self):
        self.robbery_timer.stop()
        self.rob_initiation_timer.stop()
        self.animation.stop()
        
        try:
            self.animation.finished.disconnect(self._reached_recycle_bin_destination)
        except TypeError:
            pass
        self.animation.finished.connect(self._movement_finished)

        self.is_robbing = False
        self.stolen_folder_path = None
        self.folder_awaiting_robbery = None
        self.robbery_start_pos = QPoint()

    def _return_to_normal_state_after_robbery(self):
        self._set_animation("normal")
        self.can_rob_again = False
        
        delay = random.randint(ROB_COOLDOWN_MIN_MS, ROB_COOLDOWN_MAX_MS)
        self.rob_cooldown_timer.start(delay)

        self._start_normal_state_timer()
        self._start_random_event_timer()
        self._start_ad_timer() 

    def _end_rob_cooldown(self):
        self.can_rob_again = True
        if self.folder_awaiting_robbery and not self.is_robbing and not self.is_stressed: 
            self._start_rob_initiation_timer()

    def _get_random_screen_point(self):
        screen_geometry = QApplication.primaryScreen().geometry()

        rand_x = random.randint(screen_geometry.left() + 50, screen_geometry.right() - CHARACTER_SIZE.width() - 50)
        rand_y = random.randint(screen_geometry.top() + 50, screen_geometry.bottom() - CHARACTER_SIZE.height() - 50)
        return QPoint(rand_x, rand_y)

    def _calculate_direction_key(self, start_point: QPoint, end_point: QPoint):
        dx = 0
        if end_point.x() > start_point.x():
            dx = 1
        elif end_point.x() < start_point.x():
            dx = -1

        dy = 0
        if end_point.y() > start_point.y():
            dy = 1
        elif end_point.y() < start_point.y():
            dy = -1

        return (dx, dy)

    def _start_new_movement(self):
        if self.is_event_animating or self.is_talking or self.is_robbing or self.is_stressed: 
            return

        self._stop_all_activities()
        self.is_moving = True

        start_point = self.pos()
        end_point = self._get_random_screen_point()

        direction_key = self._calculate_direction_key(start_point, end_point)
        animation_to_use = self.direction_to_animation.get(direction_key, "normal")
        self._set_animation(animation_to_use)

        self.animation.setStartValue(start_point)
        self.animation.setEndValue(end_point)

        distance_vector = QVector2D(end_point - start_point)
        distance = distance_vector.length()

        pixels_per_second = random.uniform(100, 200)
        duration = (distance / pixels_per_second) * 1000

        duration = max(NORMAL_STATE_DURATION_MS_MIN, min(NORMAL_STATE_DURATION_MS_MAX, int(duration)))

        self.animation.setDuration(duration)
        self.animation.start()

    def _movement_finished(self):
        self.is_moving = False

        if self.is_robbing:
            self._start_escape_movement()
        elif self.is_stressed: 
            self._start_stressed_movement()
        else:
            self._set_animation("idle")

            if random.random() < 0.5:
                delay = random.randint(IDLE_DURATION_MS_MIN, IDLE_DURATION_MS_MAX)
                QTimer.singleShot(delay, self._start_new_movement)
            else:
                delay = random.randint(NORMAL_STATE_DURATION_MS_MIN, NORMAL_STATE_DURATION_MS_MAX)
                self._set_animation("normal")
                QTimer.singleShot(delay, self._start_new_movement)

    def _start_escape_movement(self):
        if not self.is_robbing:
            return

        self.is_moving = True

        start_point = self.pos()
        cursor_pos = QCursor.pos()

        dx_cursor = start_point.x() - cursor_pos.x()
        dy_cursor = start_point.y() - cursor_pos.y()

        escape_vector = QVector2D(dx_cursor, dy_cursor).normalized()
        
        target_x = start_point.x() + int(escape_vector.x() * 1000)
        target_y = start_point.y() + int(escape_vector.y() * 1000)

        screen_geometry = QApplication.primaryScreen().geometry()
        padding = 50
        end_x = max(screen_geometry.left() + padding, min(screen_geometry.right() - CHARACTER_SIZE.width() - padding, target_x))
        end_y = max(screen_geometry.top() + padding, min(screen_geometry.bottom() - CHARACTER_SIZE.height() - padding, target_y))

        end_point = QPoint(end_x, end_y)

        if (end_point - start_point).manhattanLength() < 50:
            end_point = self._get_random_screen_point()

        direction_key = self._calculate_direction_key(start_point, end_point)
        animation_to_use = self.robbing_direction_to_animation.get(direction_key, "stealing_down")
        self._set_animation(animation_to_use)

        self.animation.setStartValue(start_point)
        self.animation.setEndValue(end_point)

        distance_vector = QVector2D(end_point - start_point)
        distance = distance_vector.length()
        duration = (distance / ESCAPE_SPEED_PPS) * 1000
        duration = max(500, int(duration))

        self.animation.setDuration(duration)
        self.animation.start()

    def _stop_all_activities(self):
        self.animation.stop()
        self.normal_state_timer.stop()
        self.random_event_animation_timer.stop()
        self.rob_initiation_timer.stop()
        self.stress_timer.stop() 
        self.ad_timer.stop() # <-- Se detiene el temporizador de anuncios al detener todas las actividades
        
        self.is_moving = False
        self.is_event_animating = False
        self.is_talking = False

    def _start_normal_state_timer(self):
        if self.is_robbing or self.is_talking or self.is_event_animating or self.is_stressed: return 

        self._stop_all_activities()
        self.normal_state_timer.stop()
        self.is_moving = False
        self._set_animation("normal")
        delay = random.randint(NORMAL_STATE_DURATION_MS_MIN, NORMAL_STATE_DURATION_MS_MAX)
        self.normal_state_timer.start(delay)

    def _start_random_event_timer(self):
        if self.is_robbing or self.is_talking or self.is_event_animating or self.is_stressed: return 

        if self.random_event_animation_timer.isActive():
            self.random_event_animation_timer.stop()
        delay = random.randint(EVENT_TRIGGER_DELAY_MIN_MS, EVENT_TRIGGER_DELAY_MAX)
        self.random_event_animation_timer.start(delay)

    def _trigger_random_event_animation(self):
        if self.is_talking or self.is_event_animating or self.is_robbing or self.is_stressed: 
            return

        self._stop_all_activities()
        self.is_event_animating = True

        self.previous_state_was_moving_for_event = self.is_moving
        self.previous_animation_key_for_event = self.current_animation_state

        self._set_animation(EVENT_ANIMATION_KEY)
        
        QTimer.singleShot(EVENT_ANIMATION_DURATION_MS, self._return_after_event_animation)

    def _return_after_event_animation(self):
        self.is_event_animating = False

        self._start_new_movement()
        self._start_random_event_timer()
        self._start_ad_timer() # <-- Se reinicia aquí también si se detuvo antes

    def close_application(self):
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.tray_icon.hide()
        QCoreApplication.quit()

    # --- STRESS FUNCTIONS ---
    def _start_stress_state(self):
        if self.is_stressed or self.is_robbing or self.is_talking:
            QMessageBox.information(self, "Treebilini Ocupado", "Treebilini ya está ocupado o estresado.")
            return

        self._stop_all_activities()
        self.is_stressed = True
        self.is_moving = True 
        self._set_animation("stressed") 

        self.stress_timer.start(STRESS_DURATION_MS) 
        self._start_stressed_movement() 

    def _start_stressed_movement(self):
        if not self.is_stressed:
            return

        start_point = self.pos()
        end_point = self._get_random_screen_point()

        direction_key = self._calculate_direction_key(start_point, end_point)
        animation_to_use = self.stressed_direction_to_animation.get(direction_key, "stressed")
        self._set_animation(animation_to_use)

        self.animation.setStartValue(start_point)
        self.animation.setEndValue(end_point)

        distance_vector = QVector2D(end_point - start_point)
        distance = distance_vector.length()
        
        duration = (distance / STRESS_MOVEMENT_SPEED_PPS) * 1000
        self.animation.setDuration(max(100, int(duration))) 

        self.animation.start()

    def _end_stress_state(self):
        if not self.is_stressed:
            return

        self.is_stressed = False
        self._stop_all_activities() 
        QMessageBox.information(self, "Treebilini", "Treebilini ha dejado de estar estresado.")
        self._return_to_normal_state_after_action() 

    # --- ADWARE FUNCTIONS (using notifications) ---
    def _start_ad_timer(self):
        # Evita iniciar un nuevo temporizador si Treebilini está ocupado o ya hay un temporizador activo
        if self.is_robbing or self.is_stressed or self.is_talking or self.ad_timer.isActive():
            return
        
        # Define un retraso aleatorio para el próximo anuncio (entre 30 segundos y 2 minutos)
        delay = random.randint(RANDOM_AD_DELAY_MIN_MS, RANDOM_AD_DELAY_MAX_MS)
        self.ad_timer.start(delay) # Inicia el temporizador

    def _show_random_ad(self):
        ad_title = "Notificación" # Título por defecto si no se especifica otro
        ad_message = None
        ad_icon = ICON_PATH # Por defecto, usa el icono de Treebilini para la notificación

        # Decide si mostrar un anuncio de Movistar o uno genérico
        if random.random() < MOVISTAR_AD_CHANCE:
            ad_title = "¡Gran Oferta Movistar!" # Título específico para Movistar
            ad_message = "¿Viste todo lo que te da Movistar?"
            # Aquí ad_icon sigue siendo ICON_PATH porque plyer no muestra pop-up.png como contenido
        else:
            # Selecciona un anuncio genérico de la lista de tuplas (título, mensaje)
            chosen_ad_title, chosen_ad_message = random.choice(GENERIC_ADS)
            ad_title = chosen_ad_title # Usa el título elegido del anuncio genérico
            ad_message = chosen_ad_message
            # ad_icon sigue siendo ICON_PATH

        try:
            # Muestra la notificación del sistema
            notification.notify(
                title=ad_title,
                message=ad_message,
                app_name="Treebilini", # Nombre de la aplicación que aparece en la notificación
                app_icon=ad_icon, # Ruta al icono de la aplicación (Treebilini.ico)
                timeout=10 # La notificación desaparecerá después de 10 segundos
            )
        except Exception as e:
            # Manejo de errores si la notificación no se puede mostrar
            print(f"Error al mostrar la notificación: {e}")
            QMessageBox.warning(self, "Error de Notificación", "No se pudo mostrar la notificación. Asegúrate de tener 'plyer' instalado y de que tu sistema lo soporte.")
        
        # Una vez que el anuncio se ha mostrado (o ha fallado), programar el siguiente anuncio
        self._start_ad_timer()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    treebilini = Treebilini()
    treebilini.show()

    sys.exit(app.exec())
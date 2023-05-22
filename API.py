from main import Application


class API:
    __app = Application()

    @staticmethod
    def start_app():
        API.__app.run()

    #Завантажити відео
    @staticmethod
    def load_video_for_camera_n(camera_id):
        main_controller = API.__app.mainController
        train_image_net_controller = main_controller.image_net_controller
        selected_camera = train_image_net_controller.cameras[camera_id]
        selected_camera.load_video()

    # Запустити обробку зображень
    @staticmethod
    def run_cv_for_camera_n(camera_id):
        main_controller = API.__app.mainController
        train_image_net_controller = main_controller.image_net_controller
        selected_camera = train_image_net_controller.cameras[camera_id]
        selected_camera.run_cv()

    #Генерувати датасет
    @staticmethod
    def generate_dataset_for_camera_n_line_k(camera_id, line_id):
        main_controller = API.__app.mainController
        train_image_net_controller = main_controller.image_net_controller
        selected_camera = train_image_net_controller.cameras[camera_id]
        selected_line = selected_camera.lines[line_id]
        selected_line.generate_dataset()

    # Тренувати модель для дороги n, смуги k
    @staticmethod
    def train_for_camera_n_line_k(camera_id, line_id):
        main_controller = API.__app.mainController
        train_image_net_controller = main_controller.image_net_controller
        selected_camera = train_image_net_controller.cameras[camera_id]
        selected_line = selected_camera.lines[line_id]
        selected_line.train()


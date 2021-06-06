
from website import create_app

app = create_app()
class TestViews:

    def setup(self):
        app.testing = True
        self.client = app.test_client()


    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_employees(self):
        response = self.client.get('/employees')
        assert response.status_code == 200

    def test_departments(self):
        response = self.client.get('/departments')
        assert response.status_code == 200

    def test_login(self):
        response = self.client.get('/login')
        assert response.status_code == 200

    def test_sign_up(self):
        response = self.client.get('/sign-up')
        assert response.status_code == 200

    def test_employees_id(self):
        response = self.client.get('/employees/1')
        assert response.status_code == 200

    def test_employees_id_edit(self):
        response = self.client.get('/employees/1/edit')
        assert response.status_code == 200

    def test_download(self):
        response = self.client.get('/download')
        assert response.status_code == 200

    def teardown(self):
        pass
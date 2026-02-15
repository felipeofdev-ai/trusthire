from locust import HttpUser, task, between


class TrustHireUser(HttpUser):
    wait_time = between(0.2, 1.0)

    @task(4)
    def health(self):
        self.client.get('/health')

    @task(2)
    def metrics(self):
        self.client.get('/metrics')

    @task(4)
    def analyze(self):
        payload = {
            "text": "URGENT offer! Please send $300 via crypto and contact by Telegram.",
            "include_ai_analysis": False,
            "include_link_scan": False
        }
        self.client.post('/api/v1/analyze', json=payload)

import time

class ProgressTracker:
    def __init__(self, sheets_client):
        self.sheets_client = sheets_client
        self.start_time = time.time()
        self.last_update = 0
        self.stats = {'total': 0, 'processed': 0, 'success': 0, 'failed': 0, 'errors': 0}

    def update_stats(self, result):
        self.stats['processed'] += 1
        if result.get('status') == 'success':
            self.stats['success'] += 1
        elif result.get('status') == 'failed':
            self.stats['failed'] += 1
        else:
            self.stats['errors'] += 1

    def update_progress_cell(self):
        pass  # Optional
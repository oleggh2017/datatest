import time
from transfer_service import TransferService
from settings import settings


def main():
    transfer_service = TransferService()
    while True:

        transfer_service.transfer()

        time.sleep(settings.main_sleep_time)


if __name__=="__main__":
    main()
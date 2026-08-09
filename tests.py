from json import dumps
from dataclasses import dataclass

from data_extraction import (
    get_spotify_metadata,
    InvalidURLError,
    PrivateURLError,
)


@dataclass
class TestStats:
    passed: int = 0
    failed: int = 0

    def record_success(self) -> None:
        self.passed += 1

    def record_failure(self) -> None:
        self.failed += 1

    def __repr__(self):
        total_cases = self.passed + self.failed
        passed_str = f"[PASSED] {self.passed}/{total_cases}\n"
        failed_str = f"[FAILED] {self.failed}/{total_cases}\n"
        return passed_str + failed_str


def success_printer(success: bool, error: Exception | None = None) -> None:
    """Handles success / fail message printing"""
    if success:
        print("[SUCCESS]")
    else:
        print(f"[FAIL] Details: {error}")
    print()


def test_get_spotify_metadata(print_res: bool = False) -> None:
    """
    Basic testing of :func:`get_spotify_metadata`.

    Args
    ------
    print_res : if `True` the result of the valid url extraction is being printed
    """

    valid_url = (
        "https://open.spotify.com/playlist/2dzAz7hzBNqBVlAbCHJMiH?si=025cb36ade9a4436"
    )
    track_url = (
        "https://open.spotify.com/track/5QTAcxt2yjM2qR6aw3b7Cn?si=8108965b2b244b44"
    )
    private_url = (
        "https://open.spotify.com/playlist/4avHwU2FJFOU4ScVqMzu2j?si=eb36b97fa67e4f3d"
    )

    stats = TestStats()

    print(
        "========================== TESTING SPOTIFY METADATA EXTRACTION =========================="
    )

    print("Valid url testing")
    try:
        res = get_spotify_metadata(valid_url)
        if print_res:
            print(
                dumps(
                    res,
                    indent=4,
                    ensure_ascii=False,
                )
            )
        stats.record_success()
        success_printer(
            True,
        )

    except Exception as error:
        stats.record_failure()
        success_printer(
            False,
            error,
        )

    print("Track url testing")
    try:
        get_spotify_metadata(track_url)

    except InvalidURLError:
        stats.record_success()
        success_printer(
            True,
        )

    except Exception as error:
        stats.record_failure()
        success_printer(False, error)

    print("Private url testing")
    try:
        get_spotify_metadata(private_url)

    except PrivateURLError:
        stats.record_success()
        success_printer(
            True,
        )

    except Exception as error:
        stats.record_failure()
        success_printer(False, error)

    print(stats)
    print(
        "======================= END OF SPOTIFY METADATA EXTRACTION TESTING ======================="
    )


def main():
    answers : list[str] = ['y', 'n']

    verbose : bool = False
    ans0 = ""
    while ans0 not in answers:
        ans0 = input("Verbose? (y/n): ").strip().lower()
    verbose = (ans0 == 'y')
    
    ans1 = ""
    while ans1 not in answers:
        ans1 = input("Test test_get_spotify_metadata? (y/n): ").strip().lower()
    if ans1 == 'y':
        test_get_spotify_metadata(print_res=verbose)


if __name__ == "__main__":
    main()
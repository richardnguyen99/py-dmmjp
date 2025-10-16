"""
Test for actress search functionality with detailed actress data.
"""

from typing import Any, Dict

import pytest

from py_dmmjp.actress import Actress, ActressImageURL, ActressListURL
from tests.actress_test_base import ActressTestBase


class TestActressWithDetailedFields(ActressTestBase):
    """Test implementation for actress functionality with detailed data."""

    @pytest.fixture
    def actress_data(self) -> Dict[str, Any]:
        """Mock actress data for testing - detailed actress item with all fields populated."""

        return {
            "id": "1017139",
            "name": "蓮実クレア",
            "ruby": "はすみくれあ",
            "bust": "86",
            "cup": "F",
            "waist": "57",
            "hip": "87",
            "height": "158",
            "birthday": "1991-12-03",
            "blood_type": "A",
            "hobby": "ベリーダンス",
            "prefectures": "神奈川県",
            "imageURL": {
                "small": "http://pics.dmm.co.jp/mono/actjpgs/thumbnail/hasumi_kurea.jpg",
                "large": "http://pics.dmm.co.jp/mono/actjpgs/hasumi_kurea.jpg",
            },
            "listURL": {
                "digital": "https://al.fanza.co.jp/?"
                "lurl=https%3A%2F%2Fvideo.dmm.co.jp%2Fav%2Flist%2F%3Factress%3D1017139%2F&af_id=10278-996&ch=api",
                "monthly": "https://al.fanza.co.jp/?"
                "lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fmonthly%2Fpremium%2F-%2Flist%2F%3D%2Farticle%3Dactress%2Fid%3D1017139%2F&af_id=10278-996&ch=api",
                "mono": "https://al.fanza.co.jp/?"
                "lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fmono%2Fdvd%2F-%2Flist%2F%3D%2Farticle%3Dactress%2Fid%3D1017139%2F&af_id=10278-996&ch=api",
            },
        }

    def test_actress_basic_fields(self, actress_data: Dict[str, Any]) -> None:
        """Test basic actress fields (id, name, ruby)."""

        actress = Actress.from_dict(actress_data)

        assert actress.id == 1017139
        assert actress.name == "蓮実クレア"
        assert actress.ruby == "はすみくれあ"

    def test_actress_measurements(self, actress_data: Dict[str, Any]) -> None:
        """Test measurement fields (bust, waist, hip, height, cup)."""

        actress = Actress.from_dict(actress_data)

        assert actress.bust == 86
        assert actress.waist == 57
        assert actress.hip == 87
        assert actress.height == 158
        assert actress.cup == "F"

    def test_actress_personal_info(self, actress_data: Dict[str, Any]) -> None:
        """Test personal information (birthday, blood_type, hobby, prefectures)."""

        actress = Actress.from_dict(actress_data)

        assert actress.birthday == "1991-12-03"
        assert actress.blood_type == "A"
        assert actress.hobby == "ベリーダンス"
        assert actress.prefectures == "神奈川県"

    def test_actress_image_urls(self, actress_data: Dict[str, Any]) -> None:
        """Test image URL parsing (small and large images)."""

        actress = Actress.from_dict(actress_data)

        assert actress.image_url is not None
        assert (
            actress.image_url.small
            == "http://pics.dmm.co.jp/mono/actjpgs/thumbnail/hasumi_kurea.jpg"
        )
        assert (
            actress.image_url.large
            == "http://pics.dmm.co.jp/mono/actjpgs/hasumi_kurea.jpg"
        )

    def test_actress_list_urls(self, actress_data: Dict[str, Any]) -> None:
        """Test list URL parsing (digital, monthly, mono)."""

        actress = Actress.from_dict(actress_data)

        assert actress.list_url is not None
        assert "video.dmm.co.jp" in actress.list_url.digital
        assert "actress%3D1017139" in actress.list_url.digital
        assert "monthly" in actress.list_url.monthly
        assert "mono" in actress.list_url.mono

    def test_actress_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test creating actress from dictionary."""

        actress = Actress.from_dict(actress_data)

        assert isinstance(actress, Actress)
        assert actress.id == 1017139

    def test_actress_safe_int_conversion(self, actress_data: Dict[str, Any]) -> None:
        """Test safe integer conversion for measurements."""

        actress = Actress.from_dict(actress_data)

        assert actress.bust == 86
        assert actress.waist == 57
        assert actress.hip == 87
        assert actress.height == 158

    def test_actress_optional_fields(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of optional/null fields."""

        actress = Actress.from_dict(actress_data)

        assert actress.bust is not None
        assert actress.birthday is not None
        assert actress.blood_type is not None
        assert actress.hobby is not None
        assert actress.prefectures is not None

    def test_actress_nested_objects(self, actress_data: Dict[str, Any]) -> None:
        """Test nested objects (image_url, list_url)."""

        actress = Actress.from_dict(actress_data)

        assert isinstance(actress.image_url, ActressImageURL)
        assert isinstance(actress.list_url, ActressListURL)

    def test_actress_image_url_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test ActressImageURL creation from dictionary."""

        image_data = actress_data["imageURL"]
        image_url = ActressImageURL.from_dict(image_data)

        assert isinstance(image_url, ActressImageURL)
        assert "hasumi_kurea.jpg" in image_url.small
        assert "hasumi_kurea.jpg" in image_url.large

    def test_actress_list_url_from_dict(self, actress_data: Dict[str, Any]) -> None:
        """Test ActressListURL creation from dictionary."""

        list_data = actress_data["listURL"]
        list_url = ActressListURL.from_dict(list_data)

        assert isinstance(list_url, ActressListURL)
        assert "fanza.co.jp" in list_url.digital
        assert "fanza.co.jp" in list_url.monthly
        assert "fanza.co.jp" in list_url.mono

    def test_actress_empty_data_handling(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of empty or missing data."""

        empty_data = {"id": "1", "name": "Test"}
        actress = Actress.from_dict(empty_data)

        assert actress.id == 1
        assert actress.name == "Test"
        assert actress.image_url is None
        assert actress.list_url is None

    def test_actress_string_measurements(self, actress_data: Dict[str, Any]) -> None:
        """Test conversion of string measurements to integers."""

        test_data = {"id": "1", "name": "Test", "bust": "90", "height": "165"}
        actress = Actress.from_dict(test_data)

        assert actress.bust == 90
        assert actress.height == 165

    def test_actress_invalid_data_handling(self, actress_data: Dict[str, Any]) -> None:
        """Test handling of invalid data types."""

        test_data = {
            "id": "1",
            "name": "Test",
            "bust": "invalid",
            "height": "not_a_number",
        }
        actress = Actress.from_dict(test_data)

        assert actress.bust is None
        assert actress.height is None

    def test_actress_birthday_format(self, actress_data: Dict[str, Any]) -> None:
        """Test birthday format handling."""

        actress = Actress.from_dict(actress_data)

        assert actress.birthday == "1991-12-03"

        test_data = {"id": "1", "name": "Test", "birthday": "1990-01-01"}
        actress = Actress.from_dict(test_data)
        assert actress.birthday == "1990-01-01"

    def test_actress_cup_size_validation(self, actress_data: Dict[str, Any]) -> None:
        """Test cup size field validation."""

        actress = Actress.from_dict(actress_data)

        assert actress.cup == "F"

        test_data = {"id": "1", "name": "Test", "cup": "C"}
        actress = Actress.from_dict(test_data)
        assert actress.cup == "C"

    def test_actress_prefecture_data(self, actress_data: Dict[str, Any]) -> None:
        """Test prefecture/birthplace data."""

        actress = Actress.from_dict(actress_data)

        assert actress.prefectures == "神奈川県"

        test_data = {"id": "1", "name": "Test", "prefectures": "東京都"}
        actress = Actress.from_dict(test_data)
        assert actress.prefectures == "東京都"

    def test_actress_hobby_data(self, actress_data: Dict[str, Any]) -> None:
        """Test hobby/interests data."""

        actress = Actress.from_dict(actress_data)

        assert actress.hobby == "ベリーダンス"

        test_data = {"id": "1", "name": "Test", "hobby": "読書、映画鑑賞"}
        actress = Actress.from_dict(test_data)
        assert actress.hobby == "読書、映画鑑賞"

    def test_actress_blood_type_data(self, actress_data: Dict[str, Any]) -> None:
        """Test blood type data."""

        actress = Actress.from_dict(actress_data)

        assert actress.blood_type == "A"

        test_data = {"id": "1", "name": "Test", "blood_type": "B"}
        actress = Actress.from_dict(test_data)
        assert actress.blood_type == "B"

    def test_actress_url_formatting(self, actress_data: Dict[str, Any]) -> None:
        """Test URL formatting in image and list URLs."""

        actress = Actress.from_dict(actress_data)

        assert actress.image_url.small.startswith("http://")
        assert actress.list_url.digital.startswith("https://")

    def test_actress_complete_data_validation(
        self, actress_data: Dict[str, Any]
    ) -> None:
        """Test validation of complete actress data with all fields populated."""

        actress = Actress.from_dict(actress_data)

        assert actress.id == 1017139
        assert actress.name == "蓮実クレア"
        assert actress.ruby == "はすみくれあ"

        assert actress.bust == 86
        assert actress.cup == "F"
        assert actress.waist == 57
        assert actress.hip == 87
        assert actress.height == 158

        assert actress.birthday == "1991-12-03"
        assert actress.blood_type == "A"
        assert actress.hobby == "ベリーダンス"
        assert actress.prefectures == "神奈川県"

        assert actress.image_url is not None
        assert actress.list_url is not None

    def test_actress_measurements_are_integers(
        self, actress_data: Dict[str, Any]
    ) -> None:
        """Test that measurements are properly converted to integers from strings."""

        actress = Actress.from_dict(actress_data)

        assert isinstance(actress.bust, int)
        assert isinstance(actress.waist, int)
        assert isinstance(actress.hip, int)
        assert isinstance(actress.height, int)
        assert isinstance(actress.cup, str)

    def test_actress_url_contains_correct_id(
        self, actress_data: Dict[str, Any]
    ) -> None:
        """Test that URLs contain the correct actress ID."""

        actress = Actress.from_dict(actress_data)

        assert "actress%3D1017139" in actress.list_url.digital
        assert "id%3D1017139" in actress.list_url.monthly
        assert "id%3D1017139" in actress.list_url.mono

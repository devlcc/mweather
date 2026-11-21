import json
import shutil
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
WEATHER_URL = "https://xml.dsmg.gov.mo/c_actual_brief.xml"
UV_URL = "https://xml.dsmg.gov.mo/c_actualUVI.xml"
AIR_QUALITY_URL = "https://xml.dsmg.gov.mo/c_foreiqa.xml"


def fetch_xml(url: str) -> ET.Element:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "mweather-github-pages/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return ET.fromstring(response.read())


def required_text(element: ET.Element, path: str) -> str:
    value = element.findtext(path)
    if value is None or not value.strip():
        raise ValueError(f"Missing required XML value: {path}")
    return value.strip()


def main() -> None:
    weather_xml = fetch_xml(WEATHER_URL)
    uv_xml = fetch_xml(UV_URL)
    air_quality_xml = fetch_xml(AIR_QUALITY_URL)

    weather = weather_xml.find("./Custom")
    uv_report = uv_xml.find("./Custom/ActualUVBReport")
    if weather is None or uv_report is None:
        raise ValueError("The weather or UV XML is missing its Custom report")

    air_quality_report = next(
        (
            report
            for report in air_quality_xml.findall(
                "./Custom/AQIForecastReport"
            )
            if report.find("./Station").get("code") == "AMBIENTAL"
        ),
        None,
    )
    if air_quality_report is None:
        raise ValueError("The air-quality XML has no AMBIENTAL station")

    air_quality = air_quality_report.find("./Station/AQIForecast")
    if air_quality is None:
        raise ValueError("The AMBIENTAL station has no AQI forecast")

    data = {
        "weather": {
            "iconUrl": required_text(weather, "./Icon/IconURL"),
            "description": required_text(weather, "./Icon/IconDescription"),
            "temperature": required_text(weather, "./Temperature/Value"),
            "feelsLike": required_text(weather, "./FeelsLikeDescription"),
            "humidity": required_text(weather, "./Humidity/Value"),
            "windDirection": required_text(
                weather, "./WindDirection/WindDescription"
            ),
            "windSpeed": required_text(weather, "./WindSpeed/Value"),
            "publishedAt": required_text(
                weather_xml, "./System/SysPubdate"
            ),
        },
        "uv": {
            "iconUrl": required_text(uv_report, "./Icon/IconURL"),
        },
        "airQuality": {
            "iconUrl": required_text(air_quality, "./Icon/IconURL"),
            "description": required_text(
                air_quality, "./AQIForecastDescription"
            ),
        },
    }

    OUTPUT.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "index.html", OUTPUT / "index.html")
    (OUTPUT / "weather.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Built site in dist/ with current weather, UV, and AQI data.")


if __name__ == "__main__":
    main()

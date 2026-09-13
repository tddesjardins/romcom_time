import argparse
from datetime import datetime, timedelta
import zoneinfo

NY = zoneinfo.ZoneInfo("America/New_York")
UTC = zoneinfo.ZoneInfo("UTC")


def calc_met(input_utc):
    # Return MET as decimal days since 2026-08-30T11:26:04 UTC
    reference = datetime(2026, 8, 30, 11, 26, 4, tzinfo=UTC)
    return (input_utc - reference).total_seconds() / 86400


def main():
    types = ['EASTERN', 'UTC', 'MET', 'DOY']
    parser = argparse.ArgumentParser(description="Convert between EASTERN, UTC, MET, and DOY")
    parser.add_argument("input_time", help="Input time to be converted")
    parser.add_argument("input_format", choices=types, help="Format of the input time")
    args = parser.parse_args()

    if args.input_format == 'EASTERN':
        input_edt = datetime.fromisoformat(args.input_time).replace(tzinfo=NY)
        input_utc = input_edt.astimezone(UTC)

    elif args.input_format == 'UTC':
        input_utc = datetime.fromisoformat(args.input_time).replace(tzinfo=UTC)
        input_edt = input_utc.astimezone(NY)

    elif args.input_format == 'MET':
        input_met = float(args.input_time)
        input_utc = datetime(2026, 8, 30, 11, 26, 4, tzinfo=UTC) + timedelta(days=input_met)
        input_edt = input_utc.astimezone(NY)

    elif args.input_format == 'DOY':
        doy_day, doy_clock = args.input_time.split('/')
        hour, minute, second = map(int, doy_clock.split(':'))
        input_utc = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(
            days=int(doy_day) - 1,
            hours=hour,
            minutes=minute,
            seconds=second,
        )
        input_edt = input_utc.astimezone(NY)

    input_met = calc_met(input_utc)

    doy_day = input_utc.timetuple().tm_yday
    doy_seconds = input_utc.hour * 3600 + input_utc.minute * 60 + input_utc.second
    doy_hours, remainder = divmod(doy_seconds, 3600)
    doy_minutes, doy_seconds = divmod(remainder, 60)

    # Check if the eastern time is EDT or EST based on the date and time
    if input_edt.dst() != timedelta(0):
        print(f"EASTERN (EDT): {input_edt.replace(tzinfo=None).isoformat()}")
    else:
        print(f"EASTERN (EST): {input_edt.replace(tzinfo=None).isoformat()}")
    print(f"UTC: {input_utc.replace(tzinfo=None).isoformat()}")
    print(f"MET: {input_met:.2f}")
    print(f"DOY (UTC): {doy_day}/{doy_hours:02}:{doy_minutes:02}:{doy_seconds:02}")


if __name__ == "__main__":
    main()
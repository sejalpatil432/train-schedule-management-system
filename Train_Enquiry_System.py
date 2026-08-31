import pandas as pd


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("Final_Train_Dataset_For_PowerBI.csv")

print("Dataset loaded successfully!")
print("Total train journeys:", len(df))


# ============================================================
# FORMAT JOURNEY DURATION
# ============================================================

def format_duration(hours):

    total_minutes = round(float(hours) * 60)

    h = total_minutes // 60
    m = total_minutes % 60

    return f"{h}h {m}m"


# ============================================================
# SEARCH TRAINS BY SOURCE AND DESTINATION
# ============================================================

def search_trains(source, destination):

    source = source.strip().upper()
    destination = destination.strip().upper()

    results = df[
        (df["Start_Station"].astype(str).str.strip().str.upper() == source) &
        (df["End_Station"].astype(str).str.strip().str.upper() == destination)
    ]

    return results


# ============================================================
# FIND STATION MATCHES
# ============================================================

def find_station(search_text):

    search_text = search_text.strip().upper()

    stations = sorted(
        set(df["Start_Station"].dropna()) |
        set(df["End_Station"].dropna())
    )

    matches = [
        station
        for station in stations
        if search_text in str(station).upper()
    ]

    return matches


# ============================================================
# SELECT STATION FROM MATCHING RESULTS
# ============================================================

def select_station(matches, station_type):

    if not matches:
        print(f"\nNo matching {station_type} station found.")
        return None

    # If only one station matches
    if len(matches) == 1:
        return matches[0]

    print(f"\nMatching {station_type} stations:")

    # Show maximum 20 stations
    limited_matches = matches[:20]

    for i, station in enumerate(limited_matches, start=1):
        print(f"{i}. {station}")

    if len(matches) > 20:
        print("\nShowing first 20 matches.")

    try:

        choice = int(
            input(f"\nSelect {station_type} station number: ")
        )

        if choice < 1 or choice > len(limited_matches):
            print("\nInvalid station selection.")
            return None

        return limited_matches[choice - 1]

    except ValueError:

        print("\nPlease enter a valid number.")
        return None


# ============================================================
# SEARCH TRAINS BY ROUTE
# ============================================================

def search_menu():

    print("\n========================================")
    print("          ROUTE ENQUIRY")
    print("========================================")

    # Source station
    source_input = input("\nEnter source station: ").strip()

    source_matches = find_station(source_input)

    source = select_station(
        source_matches,
        "source"
    )

    if source is None:
        return


    # Destination station
    destination_input = input(
        "\nEnter destination station: "
    ).strip()

    destination_matches = find_station(destination_input)

    destination = select_station(
        destination_matches,
        "destination"
    )

    if destination is None:
        return


    # Search direct trains
    results = search_trains(
        source,
        destination
    )


    # No direct trains
    if results.empty:

        print("\n========================================")
        print("          TRAIN SEARCH RESULTS")
        print("========================================")

        print("\nNo direct trains found.")

        print(f"Route searched:")
        print(f"{source} → {destination}")

        return


    # Display results
    print("\n========================================")
    print("          TRAIN SEARCH RESULTS")
    print("========================================")

    print(f"Source       : {source}")
    print(f"Destination  : {destination}")
    print(f"Trains Found : {len(results)}")

    print("\n----------------------------------------")


    for _, train in results.iterrows():

        print(f"\nTrain Number : {train['Train_No']}")

        print(
            f"Departure    : {train['Start_Departure']}"
        )

        print(
            f"Arrival      : {train['End_Arrival']}"
        )

        print(
            f"Distance     : {train['Total_Distance']} km"
        )

        print(
            f"Stops        : {train['Number_of_Stops']}"
        )

        print(
            f"Route Type   : {train['Route_Type']}"
        )

        print(
            f"Duration     : {format_duration(train['Journey_Hours'])}"
        )

        print("----------------------------------------")


# ============================================================
# SEARCH TRAIN BY TRAIN NUMBER
# ============================================================

def train_number_search():

    print("\n========================================")
    print("        TRAIN NUMBER ENQUIRY")
    print("========================================")

    train_no_input = input(
        "\nEnter train number: "
    ).strip()


    # Validate train number
    try:

        train_no = int(train_no_input)

    except ValueError:

        print(
            "\nInvalid train number. "
            "Please enter numbers only."
        )

        return


    # Search train
    result = df[df["Train_No"] == train_no]


    # Train not found
    if result.empty:

        print(
            f"\nNo train found with Train Number {train_no}."
        )

        return


    # Get first record
    train = result.iloc[0]


    # Display train details
    print("\n========================================")
    print(f"        TRAIN {train_no} DETAILS")
    print("========================================")

    print(
        f"Train Number : {train['Train_No']}"
    )

    print(
        f"From         : {train['Start_Station']}"
    )

    print(
        f"To           : {train['End_Station']}"
    )

    print(
        f"Departure    : {train['Start_Departure']}"
    )

    print(
        f"Arrival      : {train['End_Arrival']}"
    )

    print(
        f"Distance     : {train['Total_Distance']} km"
    )

    print(
        f"Stops        : {train['Number_of_Stops']}"
    )

    print(
        f"Route Type   : {train['Route_Type']}"
    )

    print(
        f"Duration     : {format_duration(train['Journey_Hours'])}"
    )

    print("========================================")


# ============================================================
# SHOW ALL AVAILABLE STATIONS
# ============================================================

def show_stations():

    stations = sorted(
        set(df["Start_Station"].dropna()) |
        set(df["End_Station"].dropna())
    )


    print("\n========================================")
    print("          AVAILABLE STATIONS")
    print("========================================")

    for i, station in enumerate(
        stations,
        start=1
    ):

        print(f"{i}. {station}")

    print("\n----------------------------------------")

    print(
        f"Total stations: {len(stations)}"
    )


# ============================================================
# MAIN MENU
# ============================================================

while True:

    print("\n")
    print("=" * 45)

    print(
        "          TRAIN ENQUIRY SYSTEM"
    )

    print("=" * 45)

    print("1. Search trains by route")
    print("2. Search train by train number")
    print("3. Show all stations")
    print("4. Exit")


    choice = input(
        "\nEnter your choice: "
    ).strip()


    # --------------------------------------------------------
    # OPTION 1
    # --------------------------------------------------------

    if choice == "1":

        search_menu()


    # --------------------------------------------------------
    # OPTION 2
    # --------------------------------------------------------

    elif choice == "2":

        train_number_search()


    # --------------------------------------------------------
    # OPTION 3
    # --------------------------------------------------------

    elif choice == "3":

        show_stations()


    # --------------------------------------------------------
    # OPTION 4
    # --------------------------------------------------------

    elif choice == "4":

        print(
            "\nThank you for using "
            "Train Enquiry System!"
        )

        print("Goodbye!")

        break


    # --------------------------------------------------------
    # INVALID OPTION
    # --------------------------------------------------------

    else:

        print(
            "\nInvalid choice."
        )

        print(
            "Please enter 1, 2, 3 or 4."
        )
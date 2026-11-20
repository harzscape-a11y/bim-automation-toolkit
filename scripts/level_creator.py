
# BIM Automation Toolkit
# Revit 2024 | pyRevit
# Tool 01: Automatic Level Creator

from pyrevit import revit, forms
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Level,
    Transaction
)

doc = revit.doc


def create_levels():
    instructions = (
        "Enter one level per line.\n"
        "Format: Level Name = Elevation in metres\n\n"
        "Example:\n"
        "Ground Floor = 0\n"
        "First Floor = 3.5\n"
        "Second Floor = 7\n"
        "Terrace = 10.5"
    )

    user_input = forms.ask_for_string(
        default="Ground Floor = 0\nFirst Floor = 3.5\nSecond Floor = 7\nTerrace = 10.5",
        prompt=instructions,
        title="BIM Toolkit - Level Creator"
    )

    if not user_input:
        return

    existing_levels = (
        FilteredElementCollector(doc)
        .OfClass(Level)
        .ToElements()
    )

    existing_names = [level.Name for level in existing_levels]

    created = []
    skipped = []
    errors = []

    transaction = Transaction(doc, "BIM Toolkit - Create Levels")

    transaction.Start()

    try:
        for line in user_input.splitlines():

            if "=" not in line:
                continue

            try:
                name, elevation_text = line.split("=", 1)

                name = name.strip()
                elevation_m = float(elevation_text.strip())

                if not name:
                    errors.append("Empty level name")
                    continue

                if name in existing_names:
                    skipped.append(name)
                    continue

                elevation_ft = elevation_m * 3.280839895

                level = Level.Create(doc, elevation_ft)
                level.Name = name

                existing_names.append(name)
                created.append(name)

            except Exception as error:
                errors.append("{}: {}".format(line, str(error)))

        transaction.Commit()

    except Exception:
        transaction.RollBack()
        raise

    message = "LEVEL CREATOR RESULTS\n\n"
    message += "Created: {}\n".format(len(created))
    message += "Skipped: {}\n".format(len(skipped))
    message += "Errors: {}\n\n".format(len(errors))

    if created:
        message += "Created Levels:\n"
        message += "\n".join(created)

    forms.alert(message, title="BIM Toolkit")


if __name__ == "__main__":
    create_levels()

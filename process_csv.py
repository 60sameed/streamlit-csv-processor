import csv
import datetime

def get_week_date(reader):
    format = "%d/%m/%Y"
    for row in reader:
        row_data = "".join(row).replace(".", " ").lower()
        if "created between" in row_data:
            for data in row_data.split(" "):
                try:
                    start_date = datetime.datetime.strptime(data, format)
                    break
                except:
                    pass
            
            monday = start_date + datetime.timedelta(weeks=1, days=-start_date.weekday())

            return f"{str(monday.day).zfill(2)}/{str(monday.month).zfill(2)}"
    
    return "n/a"

def process(input_file, output_file):

    with open(input_file, 'r') as input_file:
        reader = csv.reader(input_file)
        week_date = get_week_date(reader)
        
        headers = list(map(lambda h: h.lower(), next(reader)))
        job_type_index = headers.index("job type")
        insurer_index = headers.index("insurer")
        milestone_index = headers.index("milestone")
        due_on_index = headers.index("due on site date/time")
        arrived_on_index = headers.index("arrived on site date/time")

        total_number_of_instructions = 0
        cancellations = 0
        booked = 0
        empty_rows = 0
        warranty_jobs = 0

        for row in reader:
            # pre-process row
            row = list(map(lambda r: r.lower(), row))
            
            # skip the empty rows and the one having only site names
            if not "".join(row) or not "".join(row[1:]):
                empty_rows += 1
                continue

            if row[job_type_index] == "warranty": #and row[insurer_index] == "halo": is this halo check critical if yes then the count is 667
                warranty_jobs += 1
                continue
            
            
            total_number_of_instructions += 1
                
            if row[milestone_index]:
                if row[milestone_index] in ["closed", "cancelled", "deleted"]:
                    cancellations += 1
                
                elif row[due_on_index].strip() or row[arrived_on_index].strip():
                    booked += 1

    with open(output_file, 'w') as f:
        remaining = total_number_of_instructions - cancellations
        total_loss_8_percent = round(remaining - (remaining * .08)) # total loss percent should be rounded off?
        
        writer = csv.writer(f)
        writer.writerow(["Week", week_date])
        writer.writerow(["Total no. of instructions", total_number_of_instructions])
        writer.writerow(["Cancellations", cancellations])
        writer.writerow(["Remaining", remaining])
        writer.writerow(["Minus total loss (8%)", total_loss_8_percent])
        writer.writerow(["Booked", booked])
        writer.writerow(["Capture rate", f"{round(booked / total_loss_8_percent * 100)}%"])




if __name__ == "__main__":
    process("path/to/input.csv", "path/to/output.csv")
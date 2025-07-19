import re 

class dxt_parser:
    """
    A class to handle tracing of Darshan logs.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.records = []

        with open(filename, 'r') as file:
            lines = file.readlines()
            file_name = None
            for line in lines:
                p=r"#\s+DXT,\sfile_id:\s+[0-9]+,\s+file_name:\s+(.*)"
                m=re.match(p, line) # Found the start of a file trace
                if m is not None:
                    file_name = m.group(1) # Set the context to the current file name

                else:
                    p=r"\s*(\S+)\s+(\d+)\s+([a-z]+)\s+\d+\s+(\d+)\s+(\d+)\s+(\d+\.?\d*)\s+(\d+\.\d+)"
                    m=re.match(p, line) # Found a data line
                    if m is not None: 
                        record = {
                            'file_name': file_name,
                            'module': str(m.group(1)),
                            'rank': int(m.group(2)),
                            'operation': str(m.group(3)),
                            'offset': int(m.group(4)),
                            'length': int(m.group(5)),
                            'start': int(float(m.group(6))*1e+3), # Convert seconds to milliseconds
                            'end': int(float(m.group(7))*1e+3) # Convert seconds to milliseconds
                        }
                        self.records.append(record)
                        print(record)


if __name__ == "__main__": 

    parser = dxt_parser("example_darshan_trace.txt")

import json

class Heme340:
    def __init__(self):
        self.result = {
            "patient_info": {},
            "observations": []
        }

    def process(self,data):
        self.data = data
        if self.data:
            for segment in self.data:
                if segment:
                    fields = segment.split('|')
                    segment_name = fields[0]

                    if len(fields) > 2:
                        segment_type = fields[2]
                    
                        if segment_name == 'OBR' and len(fields) > 8:
                            self.result["patient_info"] = {
                                "patient_id": fields[3],
                                "name": fields[5],
                                "dob": fields[7],
                                "gender": fields[8],
                            }
                        
                        elif segment_name == 'OBX' and segment_type == "NM" and  len(fields) > 6:
                            if len(fields) > 3:
                                codeval = fields[3].split('^')[0]
                                codedesc = lambda fields:fields[3].split('^')[1] if len(fields[3].split('^')) > 1 else ''
                                observation = {
                                    "code": codeval,
                                    "description": codeval,
                                    "value": fields[5],
                                    "units": fields[6],
                                }
                                self.result["observations"].append(observation)
                                # print(observation)
                        
                        elif segment_type == "ED":
                            if len(fields) > 3:
                                codedesc = lambda fields:fields[3].split('^')[1] if len(fields[3].split('^')) > 1 else ''
                                value = fields[5].split('^')[4]                                                                            
                                observation = {
                                    "code": '',
                                    "description": fields[3].split('^')[0],
                                    "value": value,
                                    "units": '',
                                }
                                self.result["observations"].append(observation)
                                # print(observation)
        self.json_result = json.dumps(self.result, indent=4)
        return self.json_result
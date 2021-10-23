

def write_data_point(self, data_points):
    client = self.connect_to_influxdb()
    client.write_points(data_points)
    try:
        client.write_points(data_points)
    except Exception as e:
        self.module.fail_json(msg=to_native(e))

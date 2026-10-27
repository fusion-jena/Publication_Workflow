"""
Reads and Writes the necessary metrics of the documents
"""
import os


class MetricFeed:
    def write_metrics(self, directory, filename, value):
        output_dir = os.path.join(os.getcwd(), 'Data', directory)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename + '.txt')
        with open(output_path, 'a', encoding='utf-8') as output_file:
            output_file.write(value + '\n')

from customerupload.process_input import ProcessInput

processor = ProcessInput(ProcessInput.UNPROCESSED_PATH + "input-sample.tsv")
processor.execute()

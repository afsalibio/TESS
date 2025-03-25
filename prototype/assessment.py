import argparse
import queue
import json
#import numpy as np
import sounddevice as sd
import time
import winsound
#import sys
from vosk import KaldiRecognizer, Model
import jellyfish
import threading
#from file_handling import create_excel
#from audio_processing import normalize, bandpass_filter, compress

class ReadingAssessment():
    """docstring for Tess"""
    q = queue.Queue()
    def __init__(self):
        super().__init__()

    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        #if status:
            #print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l", "--list-devices", action="store_true",
        help="show list of audio devices and exit")
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        #print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        "-f", "--filename", type=str, metavar="FILENAME",
        help="audio file to store recording to")
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="input device (numeric ID or substring)")
    parser.add_argument(
        "-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    args = parser.parse_args(remaining)

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info["default_samplerate"])
            
        if args.model is None:
            model = Model(r"models\vosk-model-en-us-0.22")
        else:
            model = Model(lang=args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

    except KeyboardInterrupt:
        parser.exit(0)

    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))
    
    stop_requested = False
    skip_requested = False
    paused = False
    closing = False
    
    # Combined audio processing
    """def post_process(self, data, samplerate):
        #Normalize, bandpass filter, and compress the audio data.
        #print("post")
        # Normalize
        normalized_data = self.normalize(data)
        #print("normalize")

        # Apply bandpass filter
        filtered_data = self.bandpass_filter(normalized_data, lowcut=300, highcut=3400, samplerate=samplerate)
        #print("bandpass")
        # Apply compression
        compressed_data = self.compress(filtered_data)
        #print("compressed")

        # Ensure data type is restored back to int16 for compatibility with other systems
        processed_data = (compressed_data * 32767).astype(np.int16)

        return processed_data"""
    
    def listen_in(self):
        parser = self.parser 
        args = self.args
        try:
            with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
                    dtype="int16", channels=1, callback=self.callback):
                self.rec = KaldiRecognizer(self.model, args.samplerate)
                while True:
                    while self.paused:
                        time.sleep(0.1)
                    if self.stop_requested == True:
                        return "stop"  # Return STOP if button is clicked
                    if self.skip_requested == True:
                        self.skip_requested = False
                        return "skip"  # Return SKIP if button is clicked
                
                    data = self.q.get()

                    #processed_data = self.post_process(data, args.samplerate)
                    #print("here")

                    if self.rec.AcceptWaveform(data):
                        res = self.rec.Result()
                        res = json.loads(res)
                        fin = res.get("text", "")
                        #print (fin)
                        return(fin)
                    if self.dump_fn is not None:
                        self.dump_fn.write(data)

        except Exception as e:
            parser.exit(type(e).__name__ + ": " + str(e))

    def test_reading(self, testWord, display, timer):
        tries = 1
        status = "ongoing"
        limit = 20
        timeout = time.time() + limit
        paused_time = None

        def update_timer():
            nonlocal timeout, paused_time, status

            if status != "ongoing":
                return  # Stop updating if test ended

            if self.paused:
                if paused_time is None:
                    paused_time = time.time()  # Store when pause started
                timer.after(500, update_timer)  # Check again every 0.5s
                return  # Stop further updates

            if paused_time is not None:
                # Correct timeout only when unpausing
                timeout += time.time() - paused_time
                paused_time = None  # Reset pause tracking

            remaining = max(timeout - time.time(), 0)

            if remaining > 0:
                timer["value"] = (remaining / limit) * 100  # Update progress bar
                timer.after(1000, update_timer)  # Continue updating every sec
            else:
                timer["value"] = 0  # Ensure timer stops
                status = "stopped"  # Mark test as finished
        
        def flash_display():
            original_color = display["background"]
            display.configure(background="#d4af37")  # Change to gold
            display.after(300, lambda: display.configure(background=original_color))  # Revert after 300ms
        
        threading.Thread(target=update_timer, daemon=True).start()
        
        while status == "ongoing":
            result = self.listen_in()
            winsound.Beep(1000, 200)
            if result !="stop":
                flash_display()

            if tries == 3 :
                status = "stopped"
                return("FAIL")

            else:

                if time.time() > timeout:
                    status = "stopped"
                    return("FAIL")
                elif testWord in result:
                    status = "stopped"
                    return("CORRECT")
                elif "skip" in result:
                    status = "stopped"
                    return("FAIL")
                elif "stop" in result:
                    status = "stopped"
                    return("STOP")
                elif self.process_word(testWord,result) >= 60.0:
                    status = "stopped"
                    return ("CORRECT")

                tries = tries + 1

    def process_word(self, word, res):

        res_code = jellyfish.metaphone(res)
        word_code = jellyfish.metaphone(word)
        # Calculate Levenshtein distance between phonetic codes
        distance = jellyfish.levenshtein_distance(res_code, word_code)
        
        # Convert distance to similarity percentage
        max_len = max(len(res_code), len(word_code))
        similarity_percentage = ((max_len - distance) / max_len) * 100
        return similarity_percentage

    def fetch_reading_list(self, listNo):
        listP = ["see" , "look" , "mother" , "little" , "here" , "can" , "want" , "come" , "one" , "baby" , "three" , "run" , "jump" , "down" , "is" , "up" , "make" , "ball" , "help" , "play" ]
        list1 = ["with" , "friends" , "came" , "horse" , "ride" , "under" , "was" , "what" , "bump" , "live" , "very" , "puppy" , "dark" , "first" , "wish" , "basket" , "food" , "road" , "hill" , "along" ]
        list2 = ["game" , "hide" , "grass" , "across" , "around" , "breakfast" , "field" , "large" , "better" , "suddenly" , "happen" , "farmer" , "river" , "lunch" , "sheep" , "hope" , "forest" , "stars" , "heavy" , "station" ]
        list3 = ["safe" , "against" , "smash" , "reward" , "evening" , "stream" , "empty" , "stone" , "grove" , "desire" , "ocean" , "bench" , "damp" , "timid" , "perform" , "destroy" , "delicious" , "hunger" , "excuse" , "understood" ]
        list4 = ["harness" , "price" , "flakes" , "silence" , "develop" , "promptly" , "serious" , "courage" , "forehead" , "distant" , "anger" , "vacant" , "appearance" , "speechless" , "region" , "slumber" , "future" , "claimed" , "common" , "dainty" ]
        list5 = ["cushion" , "generally" , "extended" , "custom" , "tailor" , "haze" , "gracious" , "dignity" , "terrace" , "applause" , "jungle" , "fragrant" , "interfere" , "marriage" , "profitable" , "define" , "obedient" , "ambition" , "presence" , "merchant" ]
        list6 = ["installed" , "importance" , "medicine" , "rebellion" , "infected" , "responsible" , "liquid" , "tremendous" , "customary" , "malicious" , "spectacular" , "inventory" , "yearning" , "imaginary" , "consequently" , "excellence" , "dungeon" , "detained" , "abundant" , "compliments" ]
        list7 = ["administer" , "tremor" , "environment" , "counterfeit" , "crisis" , "industrious" , "approximate" , "society" , "architecture" , "malignant" , "pensive" , "standardize" , "exhausted" , "reminiscence" , "intricate" , "contemporary" , "attentively" , "compassionate" , "complexion" , "continuously" ]
        list8 = ["prairies" , "evident" , "nucleus" , "antique" , "twilight" , "memorandum" , "whimsical" , "proportional" , "intangible" , "formulated" , "articulate" , "deprecate" , "remarkably" , "contrasting" , "irrelevance" , "supplement" , "inducement" , "nonchalant" , "exuberant" , "grotesque" ]
        listHS = ["traverse" , "affable" , "compressible" , "excruciating" , "pandemonium" , "scrupulous" , "primordial" , "chastisement" , "sojourn" , "panorama" , "facsimile" , "auspicious" , "contraband" , "envisage" , "futility" , "enamored" , "gustatory" , "decipher" , "inadequacy" , "simultaneous" ]

        readingList = [listP , list1 , list2 , list3 , list4 , list5 , list6 , list7 , list8 , listHS ]
        current = readingList[listNo]

        new_readingList = current.copy()
        #random.shuffle(new_readingList)

        return new_readingList

    def setup_test(self, display):
        readingList = [[]] * 10
        final = readingList
        prog =0
        a = 4
        for l in range(len(readingList)):
            readingList[l] = [0, self.fetch_reading_list(l), ["FAIL"] * 20]

        final = self.test_proper(readingList, prog, display)

        return(final)

    def test_proper(self, readingList, prog, display):
        final = []  # Store the final results
        fail_limit = 10  # Maximum allowed failures

        # Iterate through each test in the reading list
        for idx, item in enumerate(readingList):
            test = item[1]  # Extract the test items for this reading
            result = ["FAIL"] * len(test)  # Initialize result list with "FAIL"
            fail_count = 0  # Counter for failures
            test_stop = False  # Flag to indicate if the test should stop

            # Process each individual test item
            for i, curr in enumerate(test):
                # Display the current test word in a separate thread
                conDisplay = threading.Thread(
                    target=self.configure_objects, args=(display, [curr.upper(), prog])
                )
                conDisplay.start()

                # Perform the test and get the result
                result_temp = self.test_reading(curr, display[0], display[2])
                result[i] = result_temp
                prog += 1

                if result_temp == "CORRECT":
                    continue  # Move to the next test item

                elif result_temp == "STOP":
                    result[i] = "FAIL"
                    test_stop = True
                    break  # Stop processing this test entirely

                elif result_temp == "FAIL":
                    fail_count += 1
                    if fail_count >= fail_limit:
                        test_stop = True
                        break  # Stop processing this test entirely

            # Calculate the score for the current test
            score = [result.count("CORRECT"), test, result]
            num_score = score[0]

            # Append the result to the final list and determine next steps
            if test_stop:
                final.append(score)  # Add the current incomplete score
                final.extend(readingList[idx + 1:])  # Append remaining untested items
                break  # Exit the loop as further tests should not be processed
            else:
                final.append(score)

        return final
    
    def configure_objects(self, display, values):
        display[0].configure(text = values[0])
        display[1].configure(value = values[1])
        return
        
    def wait_for_start(self):
        while not self.closing:
            result = self.listen_in()
            if ("start" in result) or self.process_word("start",result) >= 60.0:
                self.stop_requested = False
                return
            
    def force_stop(self):
        self.stop_requested = True
        return
    
    def force_skip(self):
        self.skip_requested = True
        return
    
    def force_pause(self):
        self.paused = True
        return
    
    def force_unpause(self):
        self.paused = False
        return
    
    def force_close(self):
        self.stop_requested = True
        self.paused = False
        self.closing = True

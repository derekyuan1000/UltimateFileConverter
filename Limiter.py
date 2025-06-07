from tkinter import filedialog
from tkinter import messagebox as mb
import Conversions as info
import os
import shutil

from PIL import Image
from pydub import AudioSegment, exceptions as pydub_exceptions

class Controller:
    def __init__(self) -> None:
        pass

    def set_gui(self,gui):
        self.gui = gui
    
    
    def update_to_format(self):
        from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        to_format = self.gui.SINGLE_FORMAT_TO_BOX
        if from_format in info.conversions:
            to_format['values'] = info.conversions[from_format]
        else:
            mb.showerror("Unrecognized Type", "You have selected a file type that is not recognized. How did you do that?")
    
    
    def update_chosen_file(self):
        input_path = filedialog.askopenfilename()
        if input_path:
            print("path chosen", input_path)
            self.gui.chosen_file.set(os.path.basename(input_path))
            self.gui.file_path = input_path

            ext = os.path.splitext(input_path)[1].lstrip('.').upper()
            if ext in info.file_formats:
                self.gui.SINGLE_FORMAT_FROM_BOX.set(ext)
                self.update_to_format()
                self.gui.lock_from_format()
            else:
                self.gui.SINGLE_FORMAT_FROM_BOX.set('')
                self.gui.unlock_from_format()

            self.gui.output_folder.set(os.path.dirname(input_path))
        else:
            self.gui.chosen_file.set("")
            self.gui.file_path = ""
            self.gui.SINGLE_FORMAT_FROM_BOX.set('')
            self.gui.unlock_from_format()

    def update_chosen_files(self):
        input_paths = filedialog.askopenfilenames()
        if input_paths:
            file_names = [os.path.basename(p) for p in input_paths]
            self.gui.chosen_files.set(", ".join(file_names))
            self.gui.file_paths = list(input_paths)

            ext = os.path.splitext(input_paths[0])[1].lstrip('.').upper()
            if ext in info.file_formats:
                self.gui.SINGLE_FORMAT_FROM_BOX.set(ext)
                self.update_to_format()
                self.gui.lock_from_format()
            else:
                self.gui.SINGLE_FORMAT_FROM_BOX.set('')
                self.gui.unlock_from_format()
            self.gui.output_folder.set(os.path.dirname(input_paths[0]))
        else:
            self.gui.chosen_files.set("")
            self.gui.file_paths = []
            self.gui.SINGLE_FORMAT_FROM_BOX.set('')
            self.gui.unlock_from_format()

    def update_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.gui.output_folder.set(folder_path)
    
    def convert_single_file(self, file_path):
        chosen_from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.SINGLE_FORMAT_TO_BOX.get()
        output_folder = self.gui.output_folder.get()
        if file_path != "":
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format,chosen_to_format):
                    if self.is_image_format(chosen_from_format) and self.is_image_format(chosen_to_format):
                        self.convert_image(file_path, chosen_to_format, output_folder)
                    elif self.is_audio_format(chosen_from_format) and self.is_audio_format(chosen_to_format):
                        self.convert_audio(file_path, chosen_to_format, output_folder)
                    else:
                        mb.showerror("Conversion not supported", "Only image and audio conversions are supported without ffmpeg.")
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")                
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected","There is no file selected. Please select a file before trying to convert.")

    def convert_single_files(self, file_paths):
        chosen_from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.SINGLE_FORMAT_TO_BOX.get()
        output_folder = self.gui.output_folder.get()
        if file_paths and len(file_paths) > 0:
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format, chosen_to_format):
                    for file_path in file_paths:
                        if self.is_image_format(chosen_from_format) and self.is_image_format(chosen_to_format):
                            self.convert_image(file_path, chosen_to_format, output_folder)
                        elif self.is_audio_format(chosen_from_format) and self.is_audio_format(chosen_to_format):
                            self.convert_audio(file_path, chosen_to_format, output_folder)
                        else:
                            mb.showerror("Conversion not supported", "Only image and audio conversions are supported without ffmpeg.")
                            break
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected", "There are no files selected. Please select files before trying to convert.")
    
    def convert_image(self, file_path, to_format, output_folder):
        try:
            out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
            with Image.open(file_path) as img:
                img.save(out_path)
            mb.showinfo("Success", f"Image converted and saved to {out_path}")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

    def convert_audio(self, file_path, to_format, output_folder):
        try:
            if not shutil.which("ffmpeg"):
                mb.showerror(
                    "FFmpeg Not Found",
                    "Audio conversion requires FFmpeg, which was not found in your system PATH. Please install FFmpeg and ensure it is accessible from the command line."
                )
                return
            out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
            audio = AudioSegment.from_file(file_path)
            audio.export(out_path, format=to_format.lower())
            mb.showinfo("Success", f"Audio converted and saved to {out_path}")
        except pydub_exceptions.CouldntDecodeError:
            mb.showerror("Error", "Could not decode audio file. Make sure FFmpeg is installed and the file is valid.")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

    def is_image_format(self, fmt):
        return fmt.upper() in ["PNG", "JPG", "JPEG", "GIF", "BMP", "WEBP", "TIFF"]

    def is_audio_format(self, fmt):
        return fmt.upper() in ["MP3", "WAV", "AAC", "OGG", "FLAC"]

    def check_file_name(self, file_path, increment, to_format, output_folder=None):
        base_name = os.path.basename(file_path)
        base, ext = os.path.splitext(base_name)
        print(base, ext)
        suffix = f"_{increment}" if increment != 0 else ""
        if output_folder:
            out_path = os.path.join(output_folder, f"{base}{suffix}.{to_format}")
        else:
            out_path = f"{base}{suffix}.{to_format}"
        if os.path.exists(out_path):
            print("Path exists", increment)
            return self.check_file_name(file_path=file_path, increment=increment + 1, to_format=to_format, output_folder=output_folder)
        else:
            return out_path
        
        
    def check_allowed_conversion(self,from_format, to_format):
        if from_format in info.conversions:
            if to_format in info.conversions[from_format]:
                return True
            else:
                return False
        else:
            return False

    def update_batch_to_format(self):
        from_format = self.gui.BATCH_FORMAT_FROM_BOX.get()
        to_format = self.gui.BATCH_FORMAT_TO_BOX
        if from_format in info.conversions:
            to_format['values'] = info.conversions[from_format]
        else:
            mb.showerror("Unrecognized Type", "You have selected a file type that is not recognized. How did you do that?")

    def update_batch_chosen_files(self):
        input_paths = filedialog.askopenfilenames()
        if input_paths:
            exts = [os.path.splitext(p)[1].lstrip('.').upper() for p in input_paths]
            if len(set(exts)) != 1:
                mb.showerror("Format Mismatch", "All selected files must have the same format.")
                self.gui.batch_chosen_files.set("")
                self.gui.batch_file_paths = []
                self.gui.BATCH_FORMAT_FROM_BOX.set('')
                self.gui.unlock_batch_from_format()
                return
            file_names = [os.path.basename(p) for p in input_paths]
            self.gui.batch_chosen_files.set(", ".join(file_names))
            self.gui.batch_file_paths = list(input_paths)

            ext = exts[0]
            if ext in info.file_formats:
                self.gui.BATCH_FORMAT_FROM_BOX.set(ext)
                self.update_batch_to_format()
                self.gui.lock_batch_from_format()
            else:
                self.gui.BATCH_FORMAT_FROM_BOX.set('')
                self.gui.unlock_batch_from_format()
            self.gui.batch_output_folder.set(os.path.dirname(input_paths[0]))
        else:
            self.gui.batch_chosen_files.set("")
            self.gui.batch_file_paths = []
            self.gui.BATCH_FORMAT_FROM_BOX.set('')
            self.gui.unlock_batch_from_format()

    def update_batch_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.gui.batch_output_folder.set(folder_path)

    def convert_batch_files(self, file_paths):
        chosen_from_format = self.gui.BATCH_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.BATCH_FORMAT_TO_BOX.get()
        output_folder = self.gui.batch_output_folder.get()
        if file_paths and len(file_paths) > 0:
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format, chosen_to_format):
                    out_folder_name = "[original image format] [export image format]"
                    out_folder_name = out_folder_name.replace(
                        "[original image format]", chosen_from_format.lower()
                    ).replace(
                        "[export image format]", chosen_to_format.lower()
                    )
                    out_folder_path = os.path.join(output_folder, out_folder_name)
                    os.makedirs(out_folder_path, exist_ok=True)
                    if self.is_image_format(chosen_from_format) and self.is_image_format(chosen_to_format):
                        self.batch_convert_images(file_paths, chosen_to_format, out_folder_path)
                    elif self.is_audio_format(chosen_from_format) and self.is_audio_format(chosen_to_format):
                        self.batch_convert_audios(file_paths, chosen_to_format, out_folder_path)
                    else:
                        mb.showerror("Conversion not supported", "Only image and audio batch conversions are supported without ffmpeg.")
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected", "There are no files selected. Please select files before trying to convert.")

    def batch_convert_images(self, file_paths, to_format, out_folder_path):
        try:
            for fp in file_paths:
                base = os.path.splitext(os.path.basename(fp))[0]
                out_path = os.path.join(out_folder_path, f"{base}.{to_format.lower()}")
                with Image.open(fp) as img:
                    img = img.convert("RGB") if to_format.upper() in ["JPG", "JPEG", "BMP"] else img
                    img.save(out_path, to_format.lower())
            mb.showinfo("Success", f"Batch images converted and saved to {out_folder_path}")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

    def batch_convert_audios(self, file_paths, to_format, out_folder_path):
        try:
            if not shutil.which("ffmpeg"):
                mb.showerror(
                    "FFmpeg Not Found",
                    "Audio conversion requires FFmpeg, which was not found in your system PATH. Please install FFmpeg and ensure it is accessible from the command line."
                )
                return
            for fp in file_paths:
                base = os.path.splitext(os.path.basename(fp))[0]
                out_path = os.path.join(out_folder_path, f"{base}.{to_format.lower()}")
                audio = AudioSegment.from_file(fp)
                audio.export(out_path, format=to_format.lower())
            mb.showinfo("Success", f"Batch audios converted and saved to {out_folder_path}")
        except pydub_exceptions.CouldntDecodeError:
            mb.showerror("Error", "Could not decode audio file. Make sure FFmpeg is installed and the file is valid.")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

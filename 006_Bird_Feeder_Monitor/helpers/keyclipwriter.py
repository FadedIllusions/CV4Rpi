# Import Needed Packages
from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2


class KeyClipWriter:
	def __init__(self, bufSize=64, timeout=1.0):
		# Store Max Buffer Size Of Frames To Be Kept In Memory
		# Along With Sleep Timeout During Threading
		self.bufSize = bufSize
		self.timeout = timeout
		
		# Init Buffer Of Frames, Queue Of Frames Needing To Be Written,
		# Video Writer, Writer Thread, Bool Indicating If Recording Started
		self.frames = deque(maxlen=bufSize)
		self.Q = None
		self.writer = None
		self.thread = None
		self.recording = False
		
	def update(self, frame):
		# Update Frames Buffer
		self.frames.appendleft(frame)
		
		# If Recording, Update Queue
		if self.recording:
			self.Q.put(frame)
			
	def start(self, outputPath, fourcc, fps):
		# Indicate We're Recording, Start Video Writer, Init Queue Of Frames
		# That Need To Be Written To Video File
		self.recording = True
		self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
									  (self.frames[0].shape[1], self.frames[0].shape[0]), True)
		self.Q = Queue()
		
		# Iterate Frames In Deque Structure And Add To Queue
		for i in range(len(self.frames), 0, -1):
			self.Q.put(self.frames[i-1])
			
		# Start Thread, Write Frames To Video File
		self.thread = Thread(target=self.write, args=())
		self.thread.daemon = True
		self.thread.start()
		
	def write(self):
		while True:
			# If Done Recording, Exit Thread
			if not self.recording:
				return
			
			# Check If Entries In Queue
			if not self.Q.empty():
				# Grab Next Frame In Queue, Write To Video File
				frame = self.Q.get()
				self.writer.write(frame)
				
			# Otherwise, Queue Empty, Sleep
			else:
				time.sleep(self.timeout)
				
	def flush(self):
		# Empty Queue By Flushing Remaining Frames To File
		while not self.Q.empty():
			frame = self.Q.get()
			self.writer.write(frame)
		
	def finish(self):
		# Indicate We're Done Recording, Join Thread, Flush Remaining 
		# Frames To File And Release The Writer Pointer
		self.recording = False
		if self.thread is not None:
			self.thread.join()
		self.flush()
		self.writer.release()
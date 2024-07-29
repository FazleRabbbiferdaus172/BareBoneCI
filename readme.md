Here's the proofread and corrected version of your text:

---

# BareBoneCi is a minimal Continuous Integration System.

The initial plan was to follow [500 Lines or Less: A Continuous Integration System](https://aosabook.org/en/500L/a-continuous-integration-system.html), but deviated a lot.

1. Wrote a multiprocess socket server class using `os.fork` and the `socket` library. This enables initiating a server that can handle multiple connections, to be used as a server for the dispatcher and runner.

## Challenges

### 1. The dummy forked server instance creation and multiprocess handling.
- Although I could have used the `socketserver` library, I wanted to code my own socket server class that uses `os.fork`.
- The first major problem I encountered was the clash between ending the loop and creating a new instance.
- While trying to solve that problem, I realized there were other problems too, like zombie processes and socket file descriptors not closing correctly.
- **This was partially solved in commit #a97101b by using `os.wait` to make the parent process wait until interruptions, closing the listening socket in the child process, and separating the start and serve methods from the constructor.**
- **Resources that helped:**
  1. [Ruslan Spivak's blog on web servers](https://ruslanspivak.com/lsbaws-part3/)
  2. [Python Fork() Exit Status](https://stonesoupprogramming.com/2017/09/07/python-fork-exit-status/)

---
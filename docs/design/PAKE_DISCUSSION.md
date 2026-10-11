Yes, I get the concept. You want the pairing to be simple and time-bounded, but not so brittle that a slow tunnel breaks it. The good news is that the "solutions in the wild" point to a clear pattern: **separate the human interaction from the technical connection window.**

Here is how you do that for the scenario you described (you on the phone, your mom across the country).

### The Core Insight: Decouple the "Code" from the "Connection"

The problem you are sensing is that the 90-second timer is currently tied to the *tunnel establishment*. You want the timer tied only to the *human coordination*.

**The Solution (Inspired by Magic Wormhole):**
Magic Wormhole uses a short, human-pronounceable code (like `4-purple-sausages`) to establish a secure channel, and it explicitly notes that the code is "single-use" and the tool waits for a short period (like 3 minutes) for the peer to connect . Crucially, once the secure channel is established, the code has served its purpose.

**How to adapt this for Grid (and your mom):**

1.  **The "Hello" Phase (90 Seconds):** Your mom's machine generates a short code. She tells you over the phone. Her machine starts a "waiting" timer (e.g., 5-10 minutes, not 90 seconds).
2.  **The "Handshake" Phase:** You enter the code on your end. Your machine uses the code to discover and authenticate with her machine (via PAKE or similar) .
3.  **The "Tunnel" Phase (No Time Pressure):** Once authentication succeeds, the *pairing window closes*. The 90-second code expires and cannot be reused. Now, your two machines have a shared secret and a valid pairing. They can spend as long as they need (seconds or minutes) to negotiate the actual WireGuard tunnel, punch through NAT, or fall back to a relay. The code is no longer needed.

The 90-second window protects the *secret* (the code). It does not need to protect the *connection*.

### The "Confirmation on the Server End" (Simplicity for Mom)

Your idea of "confirmation on the server end" is exactly right for ease of use, but it needs to be framed safely. You don't want to ask your mom to "verify cryptographic fingerprints." You want to ask her: **"Did you just try to connect to me?"**

**The Pattern in the Wild (SAS / Short Authentication Strings):**
In protocols like ZRTP or modern video conferencing, the system might display a short code (e.g., "388125") on *both* devices . The users verify the codes match.

**For Grid, simplified for a non-technical user:**
Instead of a code, when your machine attempts to pair:
1.  Your mom's machine pops a notification: **"Ryan is trying to connect. Allow?"**
2.  She clicks "Yes."
3.  The pairing succeeds.

**Why this is safe enough:** The attacker on the network doesn't know the 6-digit code. Even if they intercept the initial exchange, they cannot complete the PAKE handshake without the code. Your mom's "Allow" click is the final human confirmation . This is a classic "In-band verification" technique .

### Solutions in the Wild (What to Borrow)

1.  **Magic Wormhole's "Transit Relay" Fallback:** This is the closest match to your need. If direct connection fails, it falls back to a "Transit Relay" that just glues two TCP connections together . Your design's "Relay" is the same concept. The key is that the *initial connection* to the relay doesn't need the code—it just needs the rendezvous point.
2.  **WireGuard's "Handshake Re-initiation":** WireGuard doesn't just give up if a handshake is delayed. It has a "stopped hearing back" timer (~15s) after which it re-initiates the handshake, rather than waiting out the entire 180-second session timeout . This is a great model for your "tunnel may take a bit" concern. The agent should actively retry the tunnel establishment in the background *after* the PAKE succeeds, without needing the user to re-enter the code.
3.  **QR Codes for Speed (Optional):** If your mom's device has a camera, a QR code can contain the discovery info (IP/port) and the PAKE secret, automating the first step entirely . This eliminates the "reading the code over the phone" step, which is the most error-prone part.

### Concrete Design Proposal for Grid

**1. Pairing Code:** 6 digits (or a short word list like Magic Wormhole ).
**2. The "Waiting" Window:** When your mom initiates a pairing, her agent waits for **10 minutes** (not 90 seconds). This window is for the *human coordination*, not the tunnel.
**3. The Tunnel Window:** Once the PAKE exchange completes (which happens in milliseconds once you enter the code), the code is consumed. The agents now have a shared key and can attempt the WireGuard handshake for as long as the network allows (with retries every ~15-30 seconds if needed ).
**4. Server-Side Confirmation:** For your mom, the agent UI shows a big "Allow Ryan?" button when you attempt to connect. This is the human verification step, replacing the need for her to understand the code's security implications .

This gives you the "easy" (a 6-digit code or QR scan for you, a simple "Allow" click for her) and the "robust" (no 90-second timer killing a slow tunnel), and it borrows directly from the proven patterns of Magic Wormhole, WireGuard, and standard device pairing UX.

import time
from qcrypto.kem import KyberKEM
from rich.console import Console
console = Console()

def pause():
    console.print("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    input()

def step(msg):
    console.print(f"\n[bold magenta]💫 {msg}[/bold magenta]")
    time.sleep(0.4)
    pause()

def show(label, value, max_len=32):
    display = value.hex()[:max_len] + "..."
    console.print(f"[yellow]{label}:[/yellow] [dim]{display}[/dim]")

def divider():
    console.print("\n[blue]" + "="*50 + "[/blue]")

def main():
    divider()
    console.print("[bold green]🔐 Kyber Demo Encryption[/bold green]")
    divider()

    # Step 1 — Alice keygen
    step("Alice generates her keypair")
    alice_kem = KyberKEM()
    kp = alice_kem.generate_keypair()
    alice_pub = kp.public_key
    alice_priv = kp.private_key
    show("Alice Public Key", alice_pub)
    show("Alice Private Key", alice_priv)

    # Step 2 — Bob prepares
    step("Bob receives Alice's public key and prepares encryption")

    # Step 3 — Bob encapsulates
    step("Bob encapsulates a shared secret using Alice's public key")
    ciphertext, bob_secret = alice_kem.encapsulate(alice_pub)
    show("Ciphertext", ciphertext)
    show("Bob's Shared Secret", bob_secret)

    # Step 4 — Alice decapsulates
    step("Alice decapsulates the ciphertext to recover the shared secret")
    alice_secret = alice_kem.decapsulate(ciphertext, alice_priv)
    show("Alice's Shared Secret", alice_secret)

    # Step 5 — Compare
    step("Comparing shared secrets...")
    if alice_secret == bob_secret:
        console.print("[bold green]✅ SUCCESS: Both secrets match![/bold green]")
    else:
        console.print("[bold red]❌ ERROR: Secrets do NOT match![/bold red]")

    # Step 6 — Simulated message encryption
    step("Using shared secret to 'encrypt' a message (demo XOR)")

    message = b"Hello from the quantum-safe future"
    encrypted = bytes([m ^ bob_secret[i % len(bob_secret)] for i, m in enumerate(message)])
    show("Encrypted Message", encrypted)

    console.print("\n[cyan]📡 Sending encrypted message over insecure channel...[/cyan]")
    pause()

    # Step 7 — Decrypt
    step("Alice decrypts the message using the same secret")
    decrypted = bytes([c ^ alice_secret[i % len(alice_secret)] for i, c in enumerate(encrypted)])

    console.print(f"\n[bold green]📨 Decrypted Message:[/bold green] {decrypted.decode()}")

    divider()
    console.print("[bold magenta]🎉 Demo complete![/bold magenta]")
    divider()

if __name__ == "__main__":
    main()
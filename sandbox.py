import time
from qcrypto.kem import Kyber
from rich import print

def pause():
    input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

def step(msg):
    print(f"\n[bold magenta]💫 {msg}[/bold magenta]")
    time.sleep(0.4)
    pause()

def show(label, value, max_len=32):
    display = value.hex()[:max_len] + "..."
    print(f"[yellow]{label}:[/yellow] [dim]{display}[/dim]")

def divider():
    print("\n[blue]" + "="*50 + "[/blue]")

def main():
    divider()
    print("[bold green]🔐 Kyber Demo Encryption[/bold green]")
    divider()

    # Step 1 — Alice keygen
    step("Alice generates her keypair")
    alice_kem = Kyber("Kyber768")
    alice_pub, alice_priv = alice_kem.keygen()
    show("Alice Public Key", alice_pub)
    show("Alice Private Key", alice_priv)

    # Step 2 — Bob prepares
    step("Bob receives Alice's public key and prepares encryption")

    # Step 3 — Bob encapsulates
    step("Bob encapsulates a shared secret using Alice's public key")
    ciphertext, bob_secret = alice_kem.encaps(alice_pub)
    show("Ciphertext", ciphertext)
    show("Bob's Shared Secret", bob_secret)

    # Step 4 — Alice decapsulates
    step("Alice decapsulates the ciphertext to recover the shared secret")
    alice_secret = alice_kem.decaps(ciphertext, alice_priv)
    show("Alice's Shared Secret", alice_secret)

    # Step 5 — Compare
    step("Comparing shared secrets...")
    if alice_secret == bob_secret:
        print("[bold green]✅ SUCCESS: Both secrets match![/bold green]")
    else:
        print("[bold red]❌ ERROR: Secrets do NOT match![/bold red]")

    # Step 6 — Simulated message encryption
    step("Using shared secret to 'encrypt' a message (demo XOR)")

    message = b"Hello from the quantum-safe future 🚀"
    encrypted = bytes([m ^ bob_secret[i % len(bob_secret)] for i, m in enumerate(message)])
    show("Encrypted Message", encrypted)

    print("\n[cyan]📡 Sending encrypted message over insecure channel...[/cyan]")
    pause()

    # Step 7 — Decrypt
    step("Alice decrypts the message using the same secret")
    decrypted = bytes([c ^ alice_secret[i % len(alice_secret)] for i, c in enumerate(encrypted)])

    print(f"\n[bold green]📨 Decrypted Message:[/bold green] {decrypted.decode()}")

    divider()
    print("[bold magenta]🎉 Demo complete![/bold magenta]")
    divider()

if __name__ == "__main__":
    main()
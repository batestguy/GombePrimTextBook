# Sumatra reader access repaired - 18 November 2026

The normal Windows account could not read either final compiled PDF. Both files
had access entries only for SYSTEM, Administrators and OWNER RIGHTS. Sumatra
displayed an error loading the workbook. Its window was also off-screen.

Restored inherited permissions on only the two compiled annual PDFs with
`icacls <exact-file> /inheritance:e`, preserving their exact approved SHA-256
hashes. The normal TOSHIBA account then successfully opened both files for reading.
Restored Sumatra's window position and visually confirmed the textbook displayed
with both book tabs present. A temporary clean Sumatra profile was used; the
user's saved profile was not reset. Only the two windowless instances previously
launched for these books were stopped.

The navigation builder stages PDFs inside a temporary directory and moves them
to the output directory. The observed private file permissions are consistent
with retaining permissions from that staging directory. To prevent recurrence
when this frozen builder is run under Codex, follow it with:

```text
python output/book-navigation/restore_pdf_read_access.py
```

Run the repair as the account that generated the PDFs. It restores the existing
parent folder's inheritance for exactly these two files and verifies their bytes
do not change. It does not alter the builder, book content, approved source
fingerprints, review register, global viewer preferences or other documents.

Final approved PDF hashes remain:

- Textbook: `9fe7ae27a7b68094423feebc4eeeec5042095c3d6761e17ea7fae078cb0f3095`
- Workbook: `7c2ee3b1c1cd772db158b7d47efca33efecca20f2de335e6845646f49e0fd677`

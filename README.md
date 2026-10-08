# Storm-Kalkulator-

The app includes calculator and help pages in German, English, Hindi, Polish,
Swiss Standard German, French, Russian, Spanish, Portuguese, Italian, Arabic,
and Hebrew. PDF reports are localized for every supported language. Bundled
Noto Sans fonts (including script-specific Devanagari, Arabic, and Hebrew
families) and their SIL Open Font Licenses are in `fonts/`.

On any calculator page, upload a UTF-8 CSV to replace the equipment list.
The required columns are `Gerätename`, `Abteilung`, `Anzahl`, `Leistung_W`,
`Power_Factor`, and `Spannung_V`; department names from any supported app
language are mapped to the active language. The importer also accepts
comma- or semicolon-delimited files and validates values before loading them.

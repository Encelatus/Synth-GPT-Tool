Synthexa


convert.py:

Der gezeigte Code definiert eine Klasse namens Conversion, die Methoden zum Konvertieren verschiedener Dateiformate in Bilder oder JSON-Daten enthält. Die Klasse hat vier Klassenmethoden, die jeweils für die Konvertierung von PDF-, PPT- (PowerPoint-Präsentationen), DOC- (Word-Dokumente) und Excel-Dateien zuständig sind. Hier ist eine Zusammenfassung dessen, was jede Methode tut:

    pdf_to_images: Diese Methode nimmt den Pfad zu einer PDF-Datei und einen Ausgabeordner entgegen (mit optionaler DPI-Einstellung, die standardmäßig auf 300 gesetzt ist). Die Methode konvertiert jede Seite der PDF-Datei in ein Bild (PNG-Format) und speichert diese im angegebenen Ausgabeordner. Dabei verwendet sie die fitz-Bibliothek, um die PDF zu öffnen und zu durchlaufen, und die PIL-Bibliothek (Image), um die Bilder zu speichern.

    ppt_to_images: Diese Methode konvertiert jede Folie einer PowerPoint-Präsentation (PPT) in ein Bild und speichert diese im angegebenen Ausgabeordner. Die genauen Bibliotheken oder Module für das Laden und Konvertieren der Präsentation sind im Code nicht eindeutig gekennzeichnet, aber es sieht so aus, als würde eine hypothetische Presentation-Klasse verwendet.

    doc_to_images: Diese Methode konvertiert den Inhalt eines Word-Dokuments (DOC) in eine Reihe von Bildern. Jedes Bild stellt eine "Seite" des Dokuments dar, wobei der Text in einem festgelegten Layout gerendert wird. Der Text wird zeilenweise durchlaufen, und wenn die maximale Zeichenanzahl pro Zeile oder die maximale Höhe der "Seite" erreicht ist, wird ein neues Bild begonnen. Die PIL-Bibliothek wird hier zum Rendern des Textes und zum Speichern der Bilder verwendet.

    excel_to_json: Diese Methode liest eine Excel-Datei und konvertiert ihren Inhalt in eine JSON-Datei. Dabei wird das pandas-Modul verwendet, um die Excel-Datei zu lesen und in ein DataFrame umzuwandeln, das dann in JSON umgewandelt und in einer Datei gespeichert wird.




data_prep.py:

Diese Funktion, data_prepare, ist dafür konzipiert, Daten aus einer Datei zu lesen, zu verarbeiten und in eine spezifizierte Ausgabeform zu bringen. Die Funktion folgt diesen Schritten:

    Überprüfung und Erstellung des Ausgabeordners: Zunächst wird überprüft, ob der angegebene Ausgabeordner existiert. Wenn er nicht existiert, wird er erstellt.

    Dateilesung und JSON-Parsing: Die Funktion öffnet eine Datei im Lesemodus ('r+'), liest ihren Inhalt als String (st) und fügt eckige Klammern hinzu, um den String in eine gültige JSON-Liste umzuwandeln (ar). Dieser modifizierte String wird dann mit json.loads(ar) geparst, um ein Python-Objekt zu erhalten, das typischerweise eine Liste von Dictionaries (data) ist.

    Datenverarbeitung: Die Funktion durchläuft jedes Dictionary in der Liste data.
        Wenn das Dictionary-Element unter dem Schlüssel "graph" leer ist (len(dic.get("graph"))==0), wird der mit dem Schlüssel "text" verbundene Wert als String zur Liste text hinzugefügt.
        Wenn das Element unter dem Schlüssel "graph" nicht leer ist, wird das gesamte Dictionary-Objekt in einem neuen Dictionary text_graph_dict gespeichert, wobei k als Schlüssel dient, der mit jedem Durchlauf inkrementiert wird.

    Speicherung der Textdaten: Alle gesammelten Textdaten aus der Liste text werden zu einem einzigen String (text_str) zusammengefügt und in einer Datei namens pdf_text.txt im Ausgabeordner gespeichert. Der Schreibmodus 'a' wird verwendet, was bedeutet, dass der Text an das Ende der Datei angehängt wird, falls sie bereits existiert.

    Rückgabe: Die Funktion gibt das Dictionary text_graph_dict zurück, das alle Dictionaries aus data enthält, die ein nicht-leeres Element unter dem Schlüssel "graph" hatten.

Im Falle einer Ausnahme während der Ausführung der Funktion wird eine Fehlermeldung gedruckt und der String "No Data" zurückgegeben.

Diese Funktion könnte zum Beispiel verwendet werden, um Textdaten aus einer strukturierten Datei zu extrahieren und separat zu speichern, während komplexere Datenstrukturen wie Graphen zur weiteren Verarbeitung in einem Dictionary gesammelt werden.




main.py:

Dieser Code definiert eine einfache Webanwendung mithilfe des Flask-Webframeworks in Python. Die Anwendung stellt zwei Endpunkte bereit, die auf HTTP POST-Anfragen reagieren:

    /v1/chat: Dieser Endpunkt erwartet eine JSON-Anfrage mit mindestens einem "query"- und einem "extensions"-Feld. Die Anfrage wird verarbeitet, indem:
        Die JSON-Daten aus der Anfrage extrahiert werden.
        Ein Abgleich (match) basierend auf dem "query"-Wert und dem "extensions"-Wert durch eine Methode find_match eines Response_class-Objekts (referenziert durch obj) durchgeführt wird.
        Eine Abfrageverfeinerungskette (chain) durch die Methode query_refiner von obj erstellt wird.
        Die run-Methode dieser Kette aufgerufen wird, wobei der text-Parameter als match und der query-Parameter als der ursprüngliche "query"-Wert aus der Anfrage gesetzt werden.
        Eine Antwort als JSON zurückgegeben wird, die das Ergebnis (res) enthält.

    /v1/upload-doc: Dieser Endpunkt erlaubt das Hochladen von Dateien. Er prüft:
        Ob eine Datei im Anfrageformular enthalten ist.
        Ob eine Datei ausgewählt wurde (der Dateiname nicht leer ist).
        Ob der Dateiname in einer vorgegebenen Liste von Dokumentnamen enthalten ist.
        Bei Erfolg wird eine Bestätigung zurückgegeben, dass die Datei erfolgreich hochgeladen wurde.




prompt.py:

Dieses Skript umfasst zwei Hauptfunktionen, image_to_text und json_to_text, die jeweils spezifische Konvertierungsaufgaben durchführen. Die Funktionen nutzen die API von OpenAI, vermutlich um Inhalte mittels künstlicher Intelligenz zu analysieren und in einen anderen Format zu konvertieren. Hier ist eine detaillierte Beschreibung der beiden Funktionen:

    image_to_text:
        Lädt ein Bild von einem angegebenen Pfad und konvertiert es in eine Base64-kodierte Zeichenkette, die in ein Bild-URL-Format umgewandelt wird, das für die API-Anfrage kompatibel ist.
        Definiert zwei unterschiedliche Prompts (prompt und prompt_2), wobei prompt_2 in der Funktion verwendet wird. Diese Prompts instruieren das KI-Modell, wie die Informationen aus dem Bild extrahiert und interpretiert werden sollen.
        Sendet eine Anfrage an die OpenAI-API mit dem KI-Modell gpt-4-vision-preview, dem vordefinierten Prompt und dem Bild in Base64-Kodierung. Die Anfrage bittet das Modell, alle lesbaren Daten im Bild zu erfassen und gegebenenfalls grafische/tabellarische Daten in einen sinnvollen Text umzuwandeln.
        Speichert die Antwort des Modells, nachdem alle Zeilenumbrüche entfernt wurden, in einer Textdatei.

    json_to_text:
        Liest eine JSON-Datei von einem angegebenen Pfad und speichert ihren Inhalt als String.
        Definiert zwei unterschiedliche Prompts (prompt_xls und prompt_xls_), wobei prompt_xls_ in der Funktion verwendet wird. Diese Prompts instruieren das KI-Modell, wie es die Informationen aus der JSON-Datei interpretieren und in einen aussagekräftigen Text umwandeln soll.
        Sendet eine Anfrage an die OpenAI-API mit dem KI-Modell gpt-4-1106-preview, dem vordefinierten Prompt und der JSON-Daten als Eingabe. Die Anfrage bittet das Modell, die Daten aus dem JSON in einen lesbaren und verständlichen Text zu konvertieren.
        Speichert die Antwort des Modells, nachdem alle Zeilenumbrüche entfernt wurden, in einer Textdatei.

Am Ende des Skripts wird eine Schleife (for i in range(40)) gezeigt, die vermutlich die image_to_text-Funktion für eine Reihe von Bildern aufruft, die auf fortlaufenden Seiten eines Dokuments (z.B. PDF) basieren könnten.




response.py:

Die Response_class-Klasse ist für die Integration mit verschiedenen APIs und Diensten konzipiert, um spezifische Aufgaben der Datenverarbeitung und Analyse durchzuführen. Hier ist eine detaillierte Erklärung der Hauptkomponenten und Methoden dieser Klasse:
Initialisierung (__init__):

    Setzt API-Schlüssel für OpenAI und Pinecone und initialisiert Verbindungen zu diesen Diensten.
    Initialisiert die OpenAIEmbeddings-Instanz, um Text in Vektoren umzuwandeln (vermutlich für die semantische Suche oder Ähnlichkeitsanalyse).
    Erstellt einen Pinecone-Index (ai-doc-reader), der wahrscheinlich für die effiziente Suche in einem großen Datensatz von Dokumenten oder Datenpunkten verwendet wird.
    Initialisiert eine Instanz von ChatOpenAI mit einem spezifischen Modell (gpt-4-1106-preview), das für generative Antworten auf Anfragen verwendet wird.

find_match-Methode:

    Nimmt einen Eingabetext (input) und einen Schlüssel (key) entgegen, der die zu durchsuchenden Datenkategorien spezifiziert.
    Wandelt den Eingabetext in Vektoren um und führt eine Abfrage im Pinecone-Index durch, um die relevantesten Übereinstimmungen basierend auf den Vektoren zu finden.
    Führt für jeden Typ in key eine Abfrage durch und speichert die Ergebnisse in einem Dictionary d, wobei der Typ der Schlüssel und der Score die Wert ist.
    Ermittelt den Typ mit dem höchsten Score und führt eine weitere Abfrage durch, um die Top-N-Übereinstimmungen zu erhalten, wobei N von der Gesamtzahl der Vektoren für diesen Typ abhängt (maximal 10).
    Kombiniert die Metadaten der Top-Übereinstimmungen in einen Ergebnisstring und gibt diesen zurück.

query_refiner-Methode:

    Definiert eine Vorlage (template) für die Anfrageverfeinerung, die darauf abzielt, tiefere und genauere Antworten von der KI zu erhalten, indem sie einen Kontext ({text}) und eine spezifische Frage ({query}) bereitstellt.
    Erstellt eine PromptTemplate-Instanz mit den Eingabevariablen und der Vorlage.
    Initialisiert eine LLMChain mit dem zuvor initialisierten ChatOpenAI-Modell und der Vorlage, die für die Verarbeitung und Beantwortung von Benutzeranfragen verwendet wird.

main_response-Methode:

    Definiert ein spezifisches Prompt, das als Kontext für die Anfrageverarbeitung dient. Dieses Prompt bittet die KI, als erfahrener Datenanalyst zu handeln und eine Analyse basierend auf einem bereitgestellten Dokument durchzuführen.
    Liest den Inhalt eines spezifischen Dokuments (ai_response.txt) und fügt es in das Prompt ein.
    Sendet eine Anfrage an das OpenAI-Modell mit dem spezifizierten Prompt und der Benutzeranfrage, um eine generierte Antwort zu erhalten.
    Gibt die generierte Antwort zurück.

Insgesamt nutzt diese Klasse fortschrittliche KI-Dienste und Algorithmen, um Benutzeranfragen zu verarbeiten, Inhalte zu analysieren und relevante, informierte Antworten zu generieren.




vector_db.py:

Die Klasse vector_DB ist für das Erstellen von Vektorrepräsentationen (Embeddings) von Dokumenten und die Speicherung dieser Embeddings in einer Pinecone-Datenbank konzipiert. Sie nutzt dabei die OpenAI-API zur Generierung der Embeddings. Hier ist ein Überblick über die wichtigsten Funktionen und Methoden dieser Klasse:
Initialisierung (__init__):

    Initialisiert die Klasse mit den API-Schlüsseln für Pinecone und OpenAI.
    Erstellt eine Instanz von OpenAIEmbeddings mit den OpenAI-API-Schlüsseln und der Organisation-ID.
    Setzt den Namen des Pinecone-Indexes, in dem die Embeddings gespeichert werden sollen, auf "ai-doc-reader".

load_docs-Methode:

    Lädt Dokumente aus einem gegebenen Verzeichnis (directory). Die Methode load eines DirectoryLoader-Objekts wird verwendet, um die Dokumente zu lesen.

split_docs-Methode:

    Teilt die Dokumente in kleinere Textabschnitte (chunks) auf, um sie effizienter verarbeiten zu können. Die Methode nutzt dabei eine spezifische chunk_size und chunk_overlap zur Steuerung der Größe und Überlappung der Textabschnitte. Diese Aufteilung kann notwendig sein, um Beschränkungen der Größe von Eingabedaten für die API oder den Embedding-Prozess zu berücksichtigen.

pinecone-Methode:

    Initialisiert die Pinecone-Verbindung mit dem gespeicherten API-Schlüssel und der Umgebungsvariable.

Dokumenten-Embedding-Methoden (doc_embedding, pdf_embedding, ppt_embedding, xls_embedding):

    Diese Methoden verarbeiten spezifische Dateitypen (DOC, PDF, PPT, XLS) zur Erstellung ihrer Vektorrepräsentationen.
    Jede Methode lädt Dokumente aus dem entsprechenden Verzeichnis, teilt sie in kleinere Abschnitte und initialisiert die Pinecone-Verbindung.
    Anschließend werden die Dokumentenabschnitte mithilfe der Pinecone.from_documents-Funktion und den OpenAIEmbeddings in Embeddings umgewandelt und im Pinecone-Index unter einem spezifischen Namespace (z.B. "DOC" oder "PDF") gespeichert.

xls_category-Methode:

    Diese Methode ist speziell für die Verarbeitung von XLS-Dokumenten in bestimmten Kategorien und für spezifische Marken gedacht.
    Sie lädt Dokumente aus Verzeichnissen, die nach Kategorien und Marken organisiert sind, erstellt deren Embeddings und speichert sie im Pinecone-Index.

In den auskommentierten Codezeilen am Ende des Skripts wird gezeigt, wie die verschiedenen Methoden zum Erstellen der Embeddings aufgerufen werden können. Derzeit ist nur der Aufruf für pdf_embedding aktiviert, was bedeutet, dass nur PDF-Dokumente verarbeitet und ihre Embeddings erstellt werden, während die anderen Methodenaufrufe auskommentiert sind.
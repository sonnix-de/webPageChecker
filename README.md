# WebPage Checker

Prüft auf Änderungen von Webseiten und sendet eine E-Mail an die angegebenen Adressen.


in der .env müssen alle notwendigen Angaben konfiguriert werden:

````

[APP]
URL=example.org
CONTENT_CACHE_FILE=oldContent.html
secondsToWait=50
recipients="info@example.org;admin@example.org"
[EMAIL]
adresse=sender@example.org
smtp_server=smtp.example.org
smtp_port=587
password=passwort4sender@excample.org

````


Wichtig ist, das die "recipients" per komma getrennt werden.
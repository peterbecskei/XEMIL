import imaplib
import email
from email.header import decode_header
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email.mime.application import MIMEApplication
# Gmail IMAP szerver beállítások
imap_server = "imap.gmail.com"
IMAP_PORT = 993  # Standard IMAP SSL port

# Gmail SMTP szerver beállítások
smtp_server = "smtp.gmail.com"
smtp_port = 587

email_user = "xxxxx@gmail.com"
email_password = "xxxx xxxx xxxx xxxx"  # Használj "App Password"-ot, ha kétlépcsős hitelesítés van
def reply(receiver_email):
    #receiver_email = "karpat.zoltan@gmail.com"
    #receiver_email = "peter.becskei@gmail.com"
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')]
    print(files)
    print(receiver_email)
    sender_email = "onefile.a.i@gmail.com"
    sender_password = "qeet qadi yyur owyr"
    subject = "XML request accepted "
    body = " A ONEFILE droid automat uzenete from python "
    # E-mail üzenet összeállítása
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Csatolmányok hozzáadása
    for f in files:  # add files to the message
        file_path = os.path.join(cwd, f)
        print(file_path)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=f)
        msg.attach(attachment)
        os.remove(file_path)
        os.remove(file_path.replace('.xml','.pdf'))
    # E-mail küldése
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Titkosított kapcsolat
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("E-mail sikeresen elküldve!")
    except Exception as e:
        print(f"Hiba történt az e-mail küldése során: {e}")

def reci():
    mail = imaplib.IMAP4_SSL(imap_server, IMAP_PORT)
    mail.login(email_user, email_password)

    # Mappa kiválasztása (általában "inbox")
    mail.select("inbox")

    # E-mailek keresése
    status, messages = mail.search(None, 'unseen subject "XML"')
    # E-mailek feldolgozása
    if status == "OK" :





        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    # typ, data = conn.store(num, "-FLAGS", "\\Seen")
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    #print(from_)
                    if subject == "XML" :
                        print("futtat XML")
                        #email_body = msg_data[0][1]
                        #mail = email.message_from_bytes(email_body)
                        #if mail.get_content_maintype() != 'multipart':
                         #   return
                        for part in msg.walk():
                            if part.get_content_maintype() != 'multipart' and part.get( 'Content-Disposition') is not None : # and part.get_filename().endswith('.pdf'):
                                filename, encoding = decode_header(part.get_filename())[0]
                                print(f"csatolmány {filename}  mentése kódolás: {encoding}  ")
                                if (encoding is None):
                                    open(cwd + '/' + filename, 'wb').write(part.get_payload(decode=True))
                                else:
                                    open(cwd + '/' + filename.decode(encoding), 'wb').write(part.get_payload(decode=True))
                                                #if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None and part.get_filename().endswith('.pdf'):
                                                 #   file_path = os.path.join(cwd, part.get_filename())
                                                  #  with open(file_path, 'wb', encoding='utf-8')) as f:
                                                   #
                                    print(f"csatolmány mentve {cwd + '/' + filename.decode(encoding)}")
                        os.system("pdfopenx.exe") # futtato2.bat")
                        #os.system("XMLIST3.exe")  # futtato2.bat")
                        time.sleep(6)
                        reply(from_)
                    print(f"Téma: {subject}")
                    print(f"Feladó: {from_}")

                    #print(from_)
                    # print(data)
                    print("="*50)
    else:
        print("Nincs üzenet.")
    # Kilépés
    #print("logut.")
    mail.logout()
    print("logut. end")
#reci()
#os.system("C:/py/sendtabs 2") # futta  to2.bat")
d = time.gmtime()
time.sleep(2)
os.chdir("C:/XML/")
cwd = os.getcwd()
print( os.getcwd())
print(d)
if __name__ == '__main__':
    d = time.gmtime()
    print(
        d)  # time.struct_time(tm_year=2021, tm_mon=6, tm_mday=6, tm_hour=10, tm_min=0, tm_sec=0, tm_wday=6, tm_yday=157, tm_isdst=0)
    # h0 = d.tm_hour
    # h=h0
    # m0 = d.tm_min
    # m=m0
    while d.tm_wday <= 6:  # and m < m0 :
        print("Posta figyelés 1 percenként")
        reci()
        time.sleep(60)
        h = d.tm_hour
        m = d.tm_min
        print(f"hétfő=0 {d.tm_wday} {h}:{m}")
        d = time.gmtime()

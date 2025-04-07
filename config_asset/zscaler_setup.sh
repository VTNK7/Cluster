echo "Zscaler setup script for debian"
echo
echo "Launch in /home/vagrant directory, need zscaler.cer file in the same directory"
echo
sudo openssl x509 -inform DER -in zscaler.cer -out zscaler.crt
sudo cp zscaler.crt /usr/local/share/ca-certificates/
cd /usr/local/share/ca-certificates/
sudo update-ca-certificates
cd

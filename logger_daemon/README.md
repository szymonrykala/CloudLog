check logs: journalctl -xeu cloudlog.service
ps -aux | grep poetry

sudo systemctl daemon-reload 
sudo systemctl enable cloudlog
sudo systemctl status cloudlog
sudo systemctl start cloudlog
sudo systemctl status cloudlog

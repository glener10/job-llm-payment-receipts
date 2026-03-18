First of all install Google Drive desktop

Create a folder in Linux to mount the corresponding Google Drive folder in Windows (created only once, change "h" if needed).

```cmd
$ sudo mkdir -p /mnt/h

$ sudo mkdir -p /mnt/g
```

Mount in WSL2 using (change "h" if needed):

```cmd
sudo mount -t drvfs H: /mnt/h

sudo mount -t drvfs G: /mnt/g
```

And link dataset in Google Drive to a folder in WSL2, in root folder use:

```cmd
ln -s "/mnt/h/Meu Drive/dataset/" .

ln -s "/mnt/g/Meu Drive/PPGES/disciplinas/LIAA/dataset_just_banks_and_random_name/" .
```

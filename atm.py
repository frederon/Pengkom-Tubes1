mesinNyala = True
noATM = 0
pinATM = 0
userIndex = -1
step = 0 #0 menu utama, 1 setoran, 2 penarikan, 3 transaksi lain

users = open('dataUser.data', 'r+').readlines()
for i in range(len(users)):
  users[i] = users[i][:-1].split(",")
for i in range(len(users)):
  for j in range(len(users[i])):
    users[i][j] = int(users[i][j])

def saveState():
  f = open('dataUser.data', 'w+')
  data = ""
  for i in range(len(users)):
    for j in range(len(users[i])):
      data += str(users[i][j])
      if j != len(users[i]) - 1:
        data += ","
    data += "\n"
  f.write(data)

def printActions():
  if step == 0:
    print("1. Setoran Tunai\n2. Penarikan tunai/transaksi lain\n3. Cancel")
  elif step == 1:
    print("1. Ya\n2. Tidak")
  elif step == 2:
    print("1. Rp 100,000\n2. Rp 500,000\n3. Rp 1,000,000\n4. Rp 2,000,000\n5. Rp 2,500,000\n6. Transaksi lainnya\n7. Cancel")
  elif step == 3:
    print("1. Informasi\n2. Transfer\n3. Ganti PIN")
  printDivider()

def printDivider():
  print("=======================================================")

def formatUang(nominal):
  return "Rp " + f'{nominal:,}'

def setorUang(nominal):
  if userIndex >= 0:
    users[userIndex][2] += nominal
    return True
  return False

def tarikUang(nominal):
  if userIndex >= 0:
    if users[userIndex][2] >= nominal and nominal % 50000 == 0:
      users[userIndex][2] -= nominal
      print(formatUang(nominal) + " berhasil ditarik dari rekening Anda")
      return True
    else:
      print("Saldo Anda tidak cukup.")
      return False

def getUser(nomor):
  for i in range(len(users)):
    if nomor == int(users[i][0]):
      return i
  return - 1

def isValidPIN(nomor, pin):
  return pin == int(users[nomor][1])

def reset():
  global noATM, pinATM
  noATM = 0
  pinATM = 0
  userIndex = -1

def main():
  global mesinNyala, noATM, pinATM, userIndex, step
  while (mesinNyala):
    while (noATM == 0):
      temp = int(input("Tolong masukkan kartu atm\nNomor ATM : "))
      userIndex = getUser(temp)
      if userIndex >= 0:
        noATM = temp
      else:
        print("Nomor kartu ATM tidak ditemukan atau tidak valid. Harap coba lagi.")
        printDivider()
    while (noATM != 0 and pinATM == 0):
      printDivider()
      temp = int(input("Tolong masukkan pin ATM\nPIN ATM : "))
      if isValidPIN(userIndex, temp):
        pinATM = temp
      else:
        reset()
        print("PIN Anda salah.")
        printDivider()
    while (noATM != 0 and pinATM != 0):
      printDivider()
      saveState()
      print("Silakan memilih transaksi")
      printActions()
      commands = int(input(""))
      if commands == 1:
        step = 1
        sistemSetoran()
      elif commands == 2:
        step = 2
        sistemPenarikan()
      elif commands == 3:
        step = 0
        print("Terima kasih telah menggunakan ATM BCA!")
        printDivider()
        reset()

def sistemSetoran():
  global step
  uangMasuk = int(input("Tolong masukkan uang:\n"))
  while uangMasuk < 0 or uangMasuk % 5000 != 0:
    print("Uang yang Anda masukkan tidak valid.")
    uangMasuk = int(input("Tolong masukkan uang"))
  print("Apakah Anda yakin ingin memasukkan " + formatUang(uangMasuk) + " ke dalam rekening Anda?")
  printActions()
  commands = int(input(""))
  if commands == 1:
    if setorUang(uangMasuk):
      print(formatUang(uangMasuk) +
            " berhasil ditambahkan ke rekening Anda")
      step = 0
  elif commands == 2:
    print("Terima kasih telah menggunakan ATM BCA!")
    reset()

def sistemPenarikan():
  global step
  print("Silakan memilih transaksi")
  printActions()
  commands = int(input(""))
  if commands == 1:
    tarikUang(100000)
  elif commands == 2:
    tarikUang(500000)
  elif commands == 3:
    tarikUang(1000000)
  elif commands == 4:
    tarikUang(2000000)
  elif commands == 5:
    tarikUang(2500000)
  elif commands == 6:
    sistemTransaksiLain()
  elif commands == 7:
    reset()
  step = 0

def sistemTransaksiLain():
  global step, noATM, pinATM
  step = 3
  print("Silakan memilih transaksi")
  printActions()
  commands = int(input(""))
  if commands == 1:
    print("Nomor Rekening\t: " + str(users[userIndex][0]))
    print("Saldo\t\t: " + formatUang(users[userIndex][2]))
  elif commands == 2:
    print("Silakan memilih bank tujuan: ")
    print("1. Bank BCA\n2. Bank lain")
    printDivider()
    commands = int(input(""))
    if commands == 1:
      target = int(input("Masukkan nomor rekening BCA tujuan :\n"))
      targetIndex = getUser(target)
      if targetIndex >= 0:
        if targetIndex == userIndex:
          print("Anda tidak bisa mentransfer ke rekening Anda sendiri\n")
        else:
          nominal = int(input("Masukkan nominal transfer:\n"))
          if nominal > 0 and users[userIndex][2] >= nominal:
            users[targetIndex][2] += nominal
            users[userIndex][2] -= nominal
            print("Berhasil mentransfer sejumlah " + formatUang(nominal) + " ke nomor rekening " + str(target))
          else:
            print("Saldo tidak cukup atau nominal tidak valid.\n")
      else:
        print("Nomor rekening BCA tidak ditemukan.\n")
        printDivider()
    elif commands == 2:
      temp = int(input("Masukkan kode bank:\n"))
      target = int(input("Masukkan nomor rekening tujuan :\n"))
      print("Anda akan terkena pajak sebesar Rp 5,000 untuk melanjutkan\n")
      printDivider()
      commands = int(input("1. Ya\n2. Batal"))
      if commands == 1:
        nominal = int(input("Masukkan nominal transfer:\n"))
        if nominal > 0 and users[userIndex][2] >= nominal:
          users[userIndex][2] -= nominal + 5000
          print("Berhasil mentransfer sejumlah " +
                formatUang(nominal) + " ke kode bank " + str(temp) + " nomor rekening " + str(target))
  elif commands == 3:
    print("Masukkan PIN Anda :")
    temp = int(input(""))
    if isValidPIN(userIndex, temp):
      temp = input("Masukkan PIN baru Anda:\n")
      if len(temp) == 6:
        users[userIndex][1] = temp
        print("PIN ATM Anda berhasil diubah.")
      else:
        print("PIN ATM tidak sesuai dengan ketentuan BCA.")
    else:
      print("PIN ATM Anda tidak valid.")

main()

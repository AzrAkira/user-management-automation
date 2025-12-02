import unittest
import requests

class TestUserAPI(unittest.TestCase):
    # Alamat API kita (Target Operasi)
    BASE_URL = "http://127.0.0.1:5000/users"

    def test_1_get_all_users(self):
        """Skenario 1: Pastikan Server Hidup & Bisa Baca Data"""
        print("\n[TEST 1] Mengecek Koneksi Server...")
        
        response = requests.get(self.BASE_URL)
        
        # ASSERT: Pengecekan Kebenaran
        # Kita harapkan status code 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Kita harapkan datanya berupa List (Array)
        self.assertIsInstance(response.json(), list)
        
        print("✅ Server OK! Data berhasil diambil.")

    def test_2_lifecycle_create_delete(self):
        """Skenario 2: Siklus Hidup (Input -> Cek ID -> Hapus -> Input Lagi)"""
        print("\n[TEST 2] Menguji Siklus Create & Delete...")

        # --- LANGKAH A: INPUT DATA PERTAMA ---
        payload_1 = {
            "name": "Robot Tester 01",
            "email": "bot1@test.com",
            "company": {"name": "Skynet"}
        }
        response = requests.post(self.BASE_URL, json=payload_1)
        self.assertEqual(response.status_code, 201) # Harapannya 201 Created
        print("   -> Robot 1 berhasil dibuat.")

        # Ambil daftar terbaru untuk tahu ID si Robot 1
        # (Karena kita ambil paling atas/terbaru, dia ada di index 0)
        data_terbaru = requests.get(self.BASE_URL).json()
        robot_1 = data_terbaru[0] # Data paling atas (karena sorting DESC)
        id_robot_1 = robot_1['id']
        print(f"   -> Robot 1 mendapat ID: {id_robot_1}")

        # --- LANGKAH B: HAPUS DATA PERTAMA ---
        print(f"   -> Mencoba menghapus ID {id_robot_1}...")
        del_response = requests.delete(f"{self.BASE_URL}/{id_robot_1}")
        self.assertEqual(del_response.status_code, 200) # Harapannya 200 OK
        print("   -> Terhapus.")

        # --- LANGKAH C: INPUT DATA KEDUA (Membuktikan ID Loncat) ---
        payload_2 = {
            "name": "Robot Tester 02",
            "email": "bot2@test.com",
            "company": {"name": "Cyberdyne"}
        }
        requests.post(self.BASE_URL, json=payload_2)
        
        # Cek ID Robot 2
        data_terbaru = requests.get(self.BASE_URL).json()
        robot_2 = data_terbaru[0]
        id_robot_2 = robot_2['id']
        print(f"   -> Robot 2 berhasil dibuat. Mendapat ID: {id_robot_2}")

        # --- ASSERTION AKHIR (PEMBUKTIAN) ---
        # Memastikan ID Robot 2 LEBIH BESAR dari Robot 1 (Auto Increment jalan)
        self.assertTrue(id_robot_2 > id_robot_1)
        print(f"✅ VALIDASI SUKSES: ID tidak didaur ulang ({id_robot_1} -> {id_robot_2})")

        # Bersih-bersih (Hapus Robot 2 biar database rapi)
        requests.delete(f"{self.BASE_URL}/{id_robot_2}")

if __name__ == '__main__':
    # Verbosity=2 biar laporannya detail
    unittest.main(verbosity=2)
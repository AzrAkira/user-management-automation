import unittest
import requests

class TestUserAPI(unittest.TestCase):
    
    BASE_URL = "http://127.0.0.1:5000/users"

    def test_1_get_all_users(self):
        """Skenario 1: Pastikan Server Hidup & Bisa Baca Data"""
        print("\n[TEST 1] Mengecek Koneksi Server...")
        
        response = requests.get(self.BASE_URL)
        
       
        self.assertEqual(response.status_code, 200)
        
        
        self.assertIsInstance(response.json(), list)
        
        print("✅ Server OK! Data berhasil diambil.")

    def test_2_lifecycle_create_delete(self):
        """Skenario 2: Siklus Hidup (Input -> Cek ID -> Hapus -> Input Lagi)"""
        print("\n[TEST 2] Menguji Siklus Create & Delete...")

        
        payload_1 = {
            "name": "Robot Tester 01",
            "email": "bot1@test.com",
            "company": {"name": "Skynet"}
        }
        response = requests.post(self.BASE_URL, json=payload_1)
        self.assertEqual(response.status_code, 201) 
        print("   -> Robot 1 berhasil dibuat.")

      
        data_terbaru = requests.get(self.BASE_URL).json()
        robot_1 = data_terbaru[0] 
        id_robot_1 = robot_1['id']
        print(f"   -> Robot 1 mendapat ID: {id_robot_1}")

        
        print(f"   -> Mencoba menghapus ID {id_robot_1}...")
        del_response = requests.delete(f"{self.BASE_URL}/{id_robot_1}")
        self.assertEqual(del_response.status_code, 200) 
        print("   -> Terhapus.")

       
        payload_2 = {
            "name": "Robot Tester 02",
            "email": "bot2@test.com",
            "company": {"name": "Cyberdyne"}
        }
        requests.post(self.BASE_URL, json=payload_2)
        
       
        data_terbaru = requests.get(self.BASE_URL).json()
        robot_2 = data_terbaru[0]
        id_robot_2 = robot_2['id']
        print(f"   -> Robot 2 berhasil dibuat. Mendapat ID: {id_robot_2}")

      
        self.assertTrue(id_robot_2 > id_robot_1)
        print(f"✅ VALIDASI SUKSES: ID tidak didaur ulang ({id_robot_1} -> {id_robot_2})")

       
        requests.delete(f"{self.BASE_URL}/{id_robot_2}")

if __name__ == '__main__':
    
    unittest.main(verbosity=2)

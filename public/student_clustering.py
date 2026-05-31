""" 
- student-clustering-python
- Πηγή dataset: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams?resource=download
- Όλοι οι βαθμοί είναι σε κλίμακα 0 - 100 οπότε δεν χρειάστηκε μετατροπή βαθμών"""

import pandas as pd #για ανάγνωση CSV και διαχείρηση DataFrame
from sklearn.cluster import KMeans #αλγόριθμος ομαδοποίησης φοιτητών
from sklearn.neighbors import NearestNeighbors #αλγόριθμος εύρεσης κοντινών φοιτητών
import matplotlib.pyplot as plt #για δημιουργία γραφημάτων

features = ["math score", "reading score", "writing score"] 

#συνάρτηση όπου ανοίγει το αρχείο csv και αποθηκεύεται σε ένα pandas DataFrame
def load_dataset(path="StudentsPerformance.csv"): 
  try:
    data = pd.read_csv(path) 
    return data
  except:
    print("Δεν φορτώθηκε το αρχείο")
    return None

#συνάρτηση ομαδοποίησης φοιτητών 
def cluster_students(data):
  while True:
    try:
      k = int(input("Δώσε πλήθος ομάδων από 2 μέχρι 1000:"))
      if k < 2 or k > len(data):
        print("Λάθος πλήθος, επανέλαβε")
      else:
        break
    except:
      print("Δώσε ακέραιο αριθμό ομάδων")
  
  #total = χαρακτηριστικό για clustering
  x = data[["total"]].values 

  #ορισμός αλγορίθμου kmeans
  kmeans = KMeans(n_clusters=k, n_init="auto", random_state=23)
  data["cluster"] = kmeans.fit_predict(x) #εκπαίδευση μοντέλου fit και πρόβλεψη του cluster κάθε φοιτητή

  print(f"Δημιουργήθηκαν {k} ομάδες φοιτητών\n")

  #χωρίζονται οι φοιτητές σε ομάδες και υπολογίζονται οι μέσοι όροι, κρατώντας 2 δεκαδικά ψηφία
  stats = data.groupby("cluster").agg(count=("total", "size"), mean_total=("total", "mean")).round(2)
  print("Μέσες επιδόσεις ανά ομάδα:")
  print(stats)

  #δημιουργία γραφήματος
  plt.figure(figsize=(9, 5))
  plt.scatter(range(len(data)), data["total"], c=data["cluster"], cmap="viridis", s=30, alpha=0.8)
  plt.title("Ομαδοποίηση φοιτητών")
  plt.xlabel("Cluster ID")
  plt.ylabel("Μέσος βαθμός")
  plt.colorbar(label="cluster")
  plt.tight_layout() #δεν κόβονται τίτλοι και άξονες
  plt.show()

  return data, kmeans

#εισαγωγή νέων φοιτητών
def input_new_student():
  valid_gender = ["male","female"]
  while True:
    gender = input("Gender (Male/Female): ").strip().lower() #αφαίρεση κενών και μετατροπή σε πεζά 
    if gender in valid_gender:
      break
    else:
      print("Λάθος! Επέλεξε μία από τις έγκυρες τιμές")
      print(",".join(valid_gender))

  valid_groups = ["group A","group B","group C","group D","group E"]
  while True:
    race = input("Race/Ethinicity (group A-E): ").strip()

    #Κανονικοποίηση group a → group A
    race = race.lower().replace("group", "").strip().upper()
    race = "group " + race

    if race in valid_groups:
      break
    else:
      print("Λάθος! Επέλεξε μία από τις έγκυρες τιμές")
      print(",".join(valid_groups))

  valid_edu = [
    "some high school","high school","some college","associate's degree","bachelor's degree","master's degree"
    ]
  while True:
    parent_education = input("Parental level of education (degree): ").strip()
    if parent_education in valid_edu:
      break
    else:
      print("Λάθος! Επέλεξε μία από τις έγκυρες τιμές")
      print(",".join(valid_edu))

  valid_lunch = ["standard","free/reduced"]
  while True:
    lunch = input("Lunch (standard/free-reduced): ").strip().lower()
    if lunch in valid_lunch:
      break
    else:
      print("Λάθος! Επέλεξε μία από τις έγκυρες τιμές")
      print(",".join(valid_lunch))
  
  valid_test = ["none","completed"]
  while True:
    test_prep = input("Test preparation course (none/completed): ").strip().lower()
    if test_prep in valid_test:
      break
    else:
      print("Λάθος! Επέλεξε μία από τις έγκυρες τιμές")
      print(",".join(valid_test))

  values = []
  for col in features:
    while True:
      try:
        v = int(input(f"{col} Δώσε βαθμό από 0 - 100: "))
        if v < 0 or v > 100:
          print("Λάθος βαθμός, επανέλαβε")
        else:
          values.append(v)
          break
      except ValueError:
        print("Δώσε ακέραιο σε κλίμακα 0 - 100")

  new_student ={"gender": gender,"race/ethnicity": race,"parental level of education": parent_education,"lunch": lunch,"test preparation course": test_prep,"math score": values[0],"reading score": values[1],"writing score": values[2]
  }

  print("\n Τα δεδομένα καταχωρήθηκαν")
  return new_student

#συνάρτηση που φέρνει N κοντινούς από την ίδια ομάδα
def new_student_neighbors(new_data, data):
  #αφαίρεση της τελευταίας γραμμής
  base = data.iloc[:-1]

  #χαρακτηριστικά που θα χρησιμοποιηθούν στον kΝΝ
  X = base[["math score", "reading score", "writing score"]].values

  #τιμές νέου φοιτητή
  new_values = [[new_data["math score"],new_data["reading score"],new_data["writing score"]
  ]]
  
  nn = NearestNeighbors(n_neighbors=5, metric="euclidean")
  nn.fit(X)
  distances, indices = nn.kneighbors(new_values) #επιστροφή αποστάσεων και θέσεων των φοιτητών στο base

  neighbors = base.iloc[indices[0]].copy()
  neighbors["distance"] = distances[0]

  columns_to_show = ["cluster","math score","reading score","writing score","total","distance"
  ]

  print("\n Κοντινότεροι φοιτητές")
  print(neighbors[columns_to_show].reset_index(drop=True).round(2)) #αναρίθμηση σειρών και 2 δεκαδικά για τις αποστάσεις

def main():
  data = load_dataset()
  if data is None:
    return
  
  data["total"] = round((data["math score"] + data["reading score"] + data["writing score"]) /3, 2)

  data, kmeans = cluster_students(data) 

  print("\n Η ομαδοποίηση ολοκληρώθηκε")

  while True:
    answer = input("\n Πρόσθεση νέου φοιτητή; (y/n): ").strip().lower()

    if answer in ("y", "yes"):
      new_data = input_new_student()

      new_total = (new_data["math score"] + new_data["reading score"] + new_data["writing score"]) /3
      new_data["total"] = round(new_total, 2)

      #πρόβλεψη cluster νέου φοιτητή
      cluster_id = int(kmeans.predict([[new_total]])[0])
      new_data["cluster"] = cluster_id
      print(f"\n Ανήκει στην ομάδα: {cluster_id}")
      
      #προσθήκη φοιτητή στο dataset
      data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
      data.to_csv("StudentsPerformance_updated.csv", index=False)
      print("\n Ο νέος φοιτητής προστέθηκε και το αρχείο ενημερώθηκε")

      new_student_neighbors(new_data, data)
      print("\n Η διαδικασία ολοκληρώθηκε")
    elif answer in ("n", "no"):
      print("\n Η διαδικασία ολοκληρώθηκε")
      break
    else:
        print("Λάθος απάντηση! Δώσε 'y' 'yes' 'no' ή 'n'")

if __name__ == "__main__":
  main()
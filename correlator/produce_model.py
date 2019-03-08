import pandas
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
from sklearn.svm import SVC
# from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from multiprocessing import Pool
from functools import partial
from contextlib import contextmanager

from pyspark.sql import SparkSession
from pyspark.sql.types import *

threat_loc_file = "checkpoint_threat.csv"
shodan_file = "shodan.csv"

spss = SparkSession.builder.appName('armana').getOrCreate()

threat_sppd = spss.read.csv(threat_loc_file, inferSchema=True, header=True)
shodan_sppd = spss.read.csv(shodan_file, inferSchema=True, header=True)

# drop useless column and fill na
threat_sppd = threat_sppd.drop('atk_type')
threat_sppd = threat_sppd.fillna('na')

shodan_sppd = shodan_sppd.filter(shodan_sppd.ip.isNotNull())
shodan_sppd = shodan_sppd.filter(shodan_sppd.longitude.isNotNull())
shodan_sppd = shodan_sppd.filter(shodan_sppd.latitude.isNotNull())


def distance(instance1, instance2):
    # just in case, if the instances are lists or tuples:
    instance1 = np.array(instance1)
    instance2 = np.array(instance2)
    error = np.square(instance1 - instance2)
    return np.sqrt(np.sum(error))


def get_neighbors(test_instance, training_set, distance=distance):
    """
    get_neighors calculates a list of the k nearest neighbors
    of an instance 'test_instance'.
    The list neighbors contains 3-tuples with  
    (index, dist, label)
    where 
    index    is the index from the training_set, 
    dist     is the distance between the test_instance and the 
             instance training_set[index]
    distance is a reference to a function used to calculate the 
             distances
    """
    k = 1
    distances = []
    for index in range(len(training_set)):
        dist = distance(test_instance, training_set[index, 1:])
        distances.append((training_set[index], dist))
    distances.sort(key=lambda x: x[1])
    neighbors = distances[:k]
    return neighbors


@contextmanager
def poolcontext(*args, **kwargs):
    pool = Pool(*args, **kwargs)
    yield pool
    pool.terminate()


threat_pd = threat_sppd.toPandas()
threat_pd = threat_pd.loc[threat_pd['dst_country'] == 'United States']

shodan_pd = shodan_sppd.toPandas()

train = np.array(shodan_pd[['id', 'latitude', 'longitude']])
test = np.array(threat_pd[['dst_latitude', 'dst_longitude']])


# the get neighbors will return in index, latitude, longitude;
# create
with poolcontext(processes=4) as pool:
    results = pool.map(partial(get_neighbors, training_set=train), test)


def get_shodan_threat(oneResult):
    return oneResult[0][0][0]


with poolcontext(processes=4) as pool:
    shodan_threat_index = pool.map(get_shodan_threat, results)

shodan_threat_banner = shodan_pd[shodan_pd['id'].isin(shodan_threat_index)]
shodan_threat_banner.to_csv('shodan_threat_banner.csv')


shodan_not_threat_pd = shodan_pd[~shodan_pd['id'].isin(shodan_threat_index)]
shodan_not_threat_pd['threat'] = pandas.Series(
    0, index=shodan_not_threat_pd.index)
shodan_threat_banner['threat'] = pandas.Series(
    1, index=shodan_threat_banner.index)
shodan_threat_banner = shodan_threat_banner.append(shodan_not_threat_pd)


shodan_threat_banner_en = shodan_threat_banner[['product', 'ip_str', 'org',
                                                'transport', 'isp',
                                                'country_code_3', 'postal_code', 'dma_code', 'area_code', ]]

shodan_tmp = shodan_threat_banner[['port', 'longitude', 'latitude', 'threat']]
le = preprocessing.LabelEncoder()
shodan_threat_banner_en = shodan_threat_banner_en.apply(le.fit_transform)
shodan_threat_banner = shodan_tmp.join(shodan_threat_banner_en)

shodan_threat_banner = shodan_threat_banner.sample(
    frac=1).reset_index(drop=True)
shodan_train_np_X = np.array(shodan_threat_banner)
shodan_train_y = np.array(shodan_threat_banner['threat'])

# randF = RandomForestClassifier(
# n_estimators=600, max_depth=15, min_samples_leaf=2)
knnF = KNeighborsClassifier()
# logReg = LogisticRegression(
# random_state=0, solver='lbfgs', multi_class='multinomial')
svm_clf = SVC(gamma='auto', max_iter=10000)


# randF.fit(shodan_train_np_X, shodan_train_y)
knnF.fit(shodan_train_np_X, shodan_train_y)
# logReg.fit(shodan_train_np_X, shodan_train_y)
svm_clf.fit(shodan_train_np_X, shodan_train_y)

# randF_file = 'random_forestml.sav'
knnF_file = 'KNN_ml.sav'
# logReg_file = 'logReg.sav'
svm_file = 'svm.sav'

# joblib.dump(randF, randF_file)
joblib.dump(knnF, knnF_file)
# joblib.dump(logReg, logReg_file)
joblib.dump(svm_clf, svm_file)
# in order to use the model
# run the following code

#model = joblib.load(filename)
# result = model.predict_proba(ENCODED_INPUT_DATA)

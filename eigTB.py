import numpy as np
import scipy.sparse as sparse
import scipy.linalg as LA
import numpy.random as rand
import sys
import numpy.core.defchararray as npc

PI = np.pi


def test_hop(hop):
    if hop.size == 0:
        raise RuntimeError('\n\nRun method set_hop_uni() or set_hop() first\n')


def test_ham(ham):
    if not ham.nnz:
        raise RuntimeError('\n\nRun method get_ham() first.\n')


def test_en(en):
    if en.size == 0:
        raise RuntimeError('\n\nRun method get_eig() or first\n')


def test_vn(vn):
    if vn.size == 0:
        raise RuntimeError('\n\nRun method get_eig(eigenvec=True)  first\n')


def test_set_ons(on):
    '''
    Check method *set_ons*.

    :raises TypeError: Parameter *on* must be a list.
    :raises ValueError: Parameter *on* must be a container of real 
      and/or complex numbers.
    '''
    if not isinstance(on, list):
        raise TypeError('\n\nParameter *on* must be a list.\n')
    if not all([isinstance(o, (int, float, complex)) for o in on]):
        raise ValueError('\n\nParameter *on* must be a container of\
                                    real and/or complex numbers.\n')


def test_print_hop(n, n_max):
    '''
    Check method *print_vec_hop*.

    :raises TypeError: Parameter *n_max* must be an integer.
    :raises ValueError: Parameter *n_max* must be a positive integer.
    '''
    if not isinstance(n, int):
        raise TypeError('\n\nParameter *n_max* must be an integer.\n')
    if n < 1 or n > n_max-1:
        raise ValueError('\n\nParameter *n_max* must be a positive integer.\n')


def test_set_hop_uni(dict_hop, n_max):
    '''
    Check method *set_hop_uni*.

    :raises TypeError: Parameter *dict_hop* must be a dictionary.
    :raises ValueError: *key* must be a natural integer (0 < key <= nth max).
    :raises ValueError: Parameter *value* must be a number.
    '''
    if not isinstance(dict_hop, dict):
        raise TypeError('\n\nParameter *dict_hop* must be a dictionary\
                                  with key "n" and value "val".\n')
    for key, val in dict_hop.items():
        if not isinstance(key, int):
            raise ValueError('\n\n*dict_hop* keys must be integers.\n')
        if not 0 < key <= n_max:
            raise ValueError('\n\n*dict_hop* keys must be between 1 and\
                                    nth max distance between sites".\n')
        if not isinstance(val, (int, float, complex)):
            raise ValueError('\n\*dict_hop* values must be numbers".\n')

def test_set_hop(dict_hop, n_max):
    '''
    Check method *set_hop*.

    :raises TypeError: Parameter *dict_hop* must be a dictionary.
    :raises ValueError: *key* must be a natural integer (0 < key <= nth max).
    :raises ValueError: *value* must be a dictionary.
    :raises TypeError:  *dict_hop* values (*dic*) must be a dictionary.
    :raises TypeError: *key* must be a real number.
    :raises ValueError: *key* must be a positive number.
    :raises ValueError: *value* must be a number.
    '''
    if not isinstance(dict_hop, dict):
        raise TypeError('\n\nParameter *dict_hop* must be a dictionary\
                                  with key "n" and value a dictionary.\n')
    for key, dic in dict_hop.items():
        if not isinstance(key, int):
            raise ValueError('\n\nParameter *dict_hop* keys must be integers.\n')
        if not 0 < key <= n_max:
            raise ValueError('\n\n*dict_hop* key must be between 1 and\
                                    nth max distance between sites".\n')
        if not isinstance(dic, dict):
            raise TypeError('\n\n*dict_hop* values must be a dictionary.\n')                                 
        for a, t in dic.items():
            if not isinstance(a, (int, float)):
                raise ValueError('\n\nAngles must be real numbers".\n')
            if a < 0. or a > 180.:
                raise ValueError('\n\nAngles must be between 0 and 180".\n')
            if not isinstance(t, (int, float, complex)):
                raise ValueError('\n\nHoppings must be numbers".\n')

def test_set_hop_nearest(dict_hop):
    '''
    Check method *set_hop_nearest*.

    :raises TypeError: Parameter *dict_hop* must be a dictionary.
    :raises ValueError: *key* must be a natural integer (0 < key <= nth max).
    :raises ValueError: *value* must be a dictionary.
    :raises TypeError:  *dict_hop* values (*dic*) must be a dictionary.
    :raises TypeError: *key* must be a real number.
    :raises ValueError: *key* must be a positive number.
    :raises ValueError: *value* must be a number.
    '''
    if not isinstance(dict_hop, dict):
        raise TypeError('\n\nParameter *dict_hop* must be a dictionary\
                                  with key "n" and value a dictionary.\n')
    for key, val in dict_hop.items():
        if not isinstance(key, bytes):
            raise ValueError('\n\nParameter *dict_hop* keys must be hopping tags.\n')
        if len(key) != 2:
            raise ValueError('\n\nkey must be of length 2".\n')
        if not isinstance(val, (int, float)):
            raise ValueError('\n\nval must be numbers".\n')

def test_set_dimerization_def(hop, dict_hop, x_bottom_left, y_bottom_left):
    '''
    Check method *set_dimerization_def*.

    :raises TypeError: Parameter *alpha* must be a number.
    :raises ValueError: Parameter *alpha* must be a positive number.
    '''
    test_hop(hop)
    if not isinstance(dict_hop, dict):
        raise TypeError('\n\nParameter *dict_hop* must be a dictionary\
                                  with binary string keys and hopping values.\n')
    for key, val in dict_hop.items():
        if not isinstance(key, bytes):
            raise TypeError('\n\nDictionary key must be a binary string of length 2.\n')
        if  len(key) != 2:
            raise ValueError('\n\nDictionary key must be a binary string of length 2.\n')
        if key not in hop['tag']:
            raise ValueError('\n\nDictionary key must be a hopping tag.\n')
        if not isinstance(val, (int, float, complex)):
            raise TypeError('\n\nDictionary value must be a number.\n')            
    if not isinstance(x_bottom_left, (int, float)):
        raise TypeError('\n\n*x_bottom_left* must be a real number.\n')
    if not isinstance(y_bottom_left, (int, float)):
        raise TypeError('\n\n*y_bottom_left* must be a real number.\n')


def test_set_hop_def(hop, dict_hop, sites):
    '''
    Check method *test_set_hop_def*.

    :raises TypeError: Parameter *dict_hop* must be a dictionary
    :raises TypeError: *dict_hop* keys must be lists.
    :raises ValueError: *dict_hop* keys must be lists of length 2.
    :raises ValueError: *dict_hop* keys must be lists of integers.
    :raises TypeError: *dict_hop* keys must be lists.
    :raises ValueError: *dict_hop* keys must be integers between 0 and sites-1.
    :raises ValueError: *dict_hop* keys must be different integers between 0 and sites-1.
    :raises TypeError: *dict_hop* values must be numbers.
    '''
    test_hop(hop)
    if not isinstance(dict_hop, dict):
        raise TypeError('\n\nParameter *dict_hop* must be a dictionary.\n')
    for key, val in dict_hop.items():
        if not isinstance(key, tuple):
            raise TypeError('\n\n*dict_hop* keys must be lists.\n')
        if len(key) != 2:
            raise TypeError('\n\n*dict_hop* keys must be lists of length 2.\n')
        if not isinstance(key[0], int) or not isinstance(key[1], int):
            raise ValueError('\n\n*dict_hop* keys must be lists of integers.\n')
        if key[0] < 0 or key[1] < 0 or key[0] > sites-1 or key[1] > sites-1:
            raise ValueError('\n\n*dict_hop* keys must be integers between 0 and sites-1.\n')
        if key[0] == key[1]:
            raise ValueError('\n\n*dict_hop* keys must be different integers between 0 and sites-1.\n')
        if not isinstance(val, (int, float, complex)):
            raise TypeError('\n\n*dict_hop* values must be numbers.\n')


def test_set_ons_def(dict_ons, sites):
    '''
    Check method *test_set_ons_def*.

    :raises TypeError: Parameter *dict_ons* must be a dictionary.
    :raises TypeError: *dict_ons* keys must be integers.
    :raises TypeError: *dict_ons* keys must be numbers.
    :raises ValueError: *dict_ons* keys must be integers between 0 and sites-1.
    '''
    if not isinstance(dict_ons, dict):
        raise TypeError('\n\nParameter *dict_ons* must be a dictionary.\n')
    for key, val in dict_ons.items():
        if not isinstance(key, int):
            raise TypeError('\n\n*dict_ons* keys must be integers.\n')
        if not isinstance(val, (int, float, complex)):
            raise TypeError('\n\n*dict_ons* values must be numbers.\n')
        if key < 0 or key > sites-1:
            raise ValueError('\n\n*dict_ons* keys must be integers between 0 and sites-1.\n')


def test_set_hop_disorder(hop, alpha):
    '''
    Check method *set_disorder_hop*.

    :raises TypeError: Parameter *alpha* must be a number.
    :raises ValueError: Parameter *alpha* must be a positive number.
    '''
    test_hop(hop)
    if not isinstance(alpha, (int, float, complex)):
        raise TypeError('\n\nParameter *alpha* must be a number.\n')
    if not alpha> 0:
        raise ValueError('\n\nParameter *alpha* must be positive.\n')


def test_set_ons_disorder(on, alpha):
    '''
    Check method *set_disorder_hop*.

    :raises TypeError: Parameter *alpha* must be a number.
    :raises ValueError: Parameter *alpha* must be a positive number.
    '''
    if not isinstance(alpha, (int, float, complex)):
        raise TypeError('\n\nParameter *alpha* must be a number.\n')
    if not alpha> 0:
        raise ValueError('\n\nParameter *alpha* must be positive.\n')


def test_get_ham(hop, complex_transpose):
    '''
    Check method *get_ham*.

    :raises TypeError: Parameter *compl_trans* must be a bool.
    '''
    test_hop(hop)
    if not isinstance(complex_transpose, bool):
        raise TypeError('\n\nParameter *complex_transpose* must be a bool.\n')


def test_get_eig(ham, eigenvec):
    '''
    Check method *get_eig*.

    :raises TypeError: Parameter *eigenvec* must be a bool.
    '''
    test_ham(ham)
    if not isinstance(eigenvec, bool):
        raise TypeError('\n\nParameter *eigenvec* must be a bool.\n')


def test_get_state_pola(vn, tag_pola, tags):
    '''
    Check method *get_state_pola*.

    :raises TypeError: Parameter *tag_pola* must be a binary string.
    :raises ValueError: Parameter *tag_pola* is not a tag.

    '''
    test_vn(vn)
    if not isinstance(tag_pola, bytes):
        raise TypeError('\n\nParameter *tag_pola* must be a binary char.\n')
    if tag_pola not in tags:
        raise ValueError('\n\nParameter *tag_pola* is not a tag.\n')


def test_get_states_en(vn, e_min, e_max):
    '''
    Check method *get_states_en*.

    :raises TypeError: Parameter *e_min* must be a real number.
    :raises TypeError: Parameter *e_max* must be a real number.
    :raises ValueError: *e_min* must be smaller than *e_max*.
    '''
    test_vn(vn)
    if not isinstance(e_min, (int, float)):
        raise TypeError('\n\nParameter *e_min* must be a real number.\n')
    if not isinstance(e_max, (int, float)):
        raise TypeError('\n\nParameter *e_max* must be a real number.\n')
    if not e_min < e_max:
        raise ValueError('\n\n*e_min* must be smaller than *e_max*.\n')


class eigTB():
    '''
    Solve the Tight-Binding eigenvalue problem of a lattice defined 
    using the class **latticeTB**.

    :param lat: **latticeTB** class instance.
    '''
    def __init__(self, lat):
        if not lat.coor.size:
           raise RuntimeError('\n\nRun method get_lattice() of latticeTB first.\n')
        self.lat = lat
        self.vec_hop = self.get_hop()
        self.dist_uni = np.unique(self.vec_hop['d'])
        self.ang_uni = np.unique(self.vec_hop['a'])
        self.coor_hop = np.array([], dtype=[ ('x','f8'), ('y','f8'), ('tag','S1')])
        self.hop = np.array([], dtype=[('i', 'u4'), ('j', 'u4'), ('t', 'c16'), ('ang', 'u2'), ('tag', 'S2')])#  Hoppings
        self.ons = np.zeros(self.lat.sites, 'c16') #  Onsite energies
        self.ham = sparse.csr_matrix(([],([],[])), shape=(self.lat.sites, self.lat.sites))  # Hamiltonian
        self.en = np.array([], 'c16')  # Eigenenergies
        self.vn = np.array([], 'c16')  # Eigenvectors
        self.intensity = np.array([], 'f8')  # Intensities (|vn|**2)
        self.pola = np.array([], 'f8')  # sublattices polarisation (|vn^{(S)}|**2)
        self.alpha = 0.  # hopping disorder strength
        self.alpha_on = 0.  # onsite disorder strength
        self.params = {}

    def get_hop(self):
        '''
        Get the distances and the angles of the hoppings.
        '''
        dif_x = self.lat.coor['x'] - self.lat.coor['x'].reshape(self.lat.sites, 1)
        dif_y = self.lat.coor['y'] - self.lat.coor['y'].reshape(self.lat.sites, 1)
        dist = np.sqrt(dif_x ** 2 + dif_y ** 2).round(3)
        ang = (180 / PI * np.arctan2(dif_y, dif_x)).round(3)
        vec_hop = np.zeros(dist.shape, dtype=[('d', 'f8'),  ('a', 'f8')])
        vec_hop['d'] = dist
        vec_hop['a'] = ang
        return vec_hop

    def print_hop(self, n=5):
        '''
        Print the distances and the angles of all hoppings.

        :param n: Positive integer. Print the first nth hoppings
          distances and associated positive angles.
        '''
        test_print_hop(n, len(self.dist_uni)-1)
        print('Distances between sites:')
        for i, d in enumerate(self.dist_uni[1:n]):
            print(i+1, d)
            print('\twith positive angles:')
            positve_ang = self.vec_hop['a'][(self.vec_hop['d'] == d) &
                                                        (self.vec_hop['a'] >= 0.)]
            print('\t', np.unique(positve_ang))

    def set_ons(self, on):
        '''
        Set onsite energies.

        :param on:  Array. Sublattice onsite energies.
        '''
        test_set_ons(on)
        self.on = on
        for o, t in zip(on, self.lat.tags):
            self.ons[self.lat.coor['tag'] == t] = o
           
    def set_hop_uni(self, dict_hop):
        '''
        Set uniform lattice hoppings.

        :param dict_hop: Dictionary with key {n} nth hopping
        :param dict_hop: Dictionary with key {n} nth hopping
          and value {val} of the hopping.
        '''
        test_set_hop_uni(dict_hop, len(self.dist_uni)-1)
        for key, t in dict_hop.items(): 
            ind = np.argwhere((self.vec_hop['d'] > self.dist_uni[key]-1e-6) &
                                       (self.vec_hop['d'] < self.dist_uni[key]+ 1e-6))
            hop = np.zeros(len(ind), dtype=[('i', 'u4'), ('j', 'u4'), ('t', 'c16'), ('ang', 'u2'), ('tag', 'S2')])
            hop['i'] = ind[:, 0]
            hop['j'] = ind[:, 1]
            hop['t'] = t
            hop['tag'] = npc.add(self.lat.coor['tag'][ind[:, 0]], self.lat.coor['tag'][ind[:, 1]])
            self.hop = np.concatenate([self.hop, hop])

    def set_hop(self, dict_hop):
        '''
        Set non uniform lattice hoppings.

        :param dict_hop: Dictionary with key a tuple:(n, 'ang'} nth hopping,
          associated positive angle, and hopping value {val}.
        '''
        test_set_hop(dict_hop, len(self.dist_uni)-1)
        
        for key, dic in dict_hop.items():
            ind = np.argwhere((self.vec_hop['d'] > self.dist_uni[key]-1e-6) &
                                       (self.vec_hop['d'] < self.dist_uni[key]+1e-6))
            ind_up = ind[ind[:, 1] > ind[:, 0]]      
            dist_x = self.lat.coor['x'][ind_up[:, 1]]-self.lat.coor['x'][ind_up[:, 0]]
            dist_y = self.lat.coor['y'][ind_up[:, 1]]-self.lat.coor['y'][ind_up[:, 0]]
            ang_up = np.round(180 / PI * np.arctan2(dist_y, dist_x), 3)
            for a, t in dic.items():
                ind_tag = ind_up[ang_up == a]
                hop = np.zeros(len(ind), dtype=[('i', 'u4'), ('j', 'u4'), ('t', 'c16'), ('ang', 'u2'), ('tag', 'S2')])
                hop['i'] = ind_tag[:, 0]
                hop['j'] = ind_tag[:, 1]
                hop['ang'] = a
                hop['t'] = t
                hop['tag'] = npc.add(self.lat.coor['tag'][ind_tag[:, 0]], self.lat.coor['tag'][ind_tag[:, 1]])
                self.hop = np.concatenate([self.hop, hop])

    def set_hop_nearest(self, dict_hop):
        '''
        Set non uniform lattice hoppings.

        :param dict_hop: Dictionary with key a tuple:(n, 'tag'} nth hopping,
          and hopping value {val}.
        '''
        test_set_hop_nearest(dict_hop)
        ind = np.argwhere((self.vec_hop['d'] > self.dist_uni[1]-1e-6) &
                                   (self.vec_hop['d'] < self.dist_uni[1]+1e-6))
        ind_up = ind[ind[:, 1] > ind[:, 0]]  
        self.hop = np.zeros(len(ind_up), dtype=[('i', 'u4'), ('j', 'u4'), ('t', 'c16'), ('ang', 'u2'), ('tag', 'S2')])
        self.hop['i'] = ind_up[:, 0]
        self.hop['j'] = ind_up[:, 1]
        self.hop['tag'] = npc.add(self.lat.coor['tag'][ind_up[:, 0]], self.lat.coor['tag'][ind_up[:, 1]])
        for s, t in dict_hop.items():
            self.hop['t'][self.hop['tag'] == s] = t

    def set_ons_def(self, dict_ons_def):
        '''
        Set specific onsite energies.

        :param dict_ons_def:  Dictionary. key: site indices, val: onsite values. 
        '''
        test_set_ons_def(dict_ons_def, self.lat.sites)
        for i, o in dict_ons_def.items():
            self.ons[i] = o

    def set_hop_def(self,dict_hop_def):
        '''
        Set specific hoppings. 

        :param dict_hop_def:  Dictionary. key: hopping indices, val: hopping values. 
        '''
        test_set_hop_def(self.hop, dict_hop_def, self.lat.sites)
        for key, val in dict_hop_def.items():
            cond = (self.hop['i'] == key[0]) & (self.hop['j'] == key[1])
            self.hop['t'][cond] = val
            cond = (self.hop['j'] == key[0]) & (self.hop['i'] == key[1])
            self.hop['t'][cond] = val

    def set_dimerization_def(self, dict_hop, x_bottom_left, y_bottom_left):
        '''
        Set a dimerization defect.

        :param dict_hop: Dictionary with key a tuple:(n, 'ang'} nth hopping,
          associated positive angle, and hopping value {val}.
        '''
        test_set_dimerization_def(self.hop, dict_hop, x_bottom_left, y_bottom_left)
        for key, val in dict_hop.items():
            ind = (self.lat.coor['x'][self.hop['i']] >= x_bottom_left) & \
                    (self.lat.coor['y'][self.hop['i']] >= y_bottom_left)
            self.hop['t'][ind & (self.hop['tag'] == key)] = val

    def  set_hop_disorder(self, alpha):
        '''
        Set a uniform hopping disorder. 

        :param alpha: Stength of the disorder.
        '''
        test_set_hop_disorder(self.hop, alpha)
        self.hop['t'] *= 1. + alpha * rand.uniform(-0.5, 0.5, len(self.hop))
        self.alpha = alpha

    def set_ons_disorder(self, alpha):
        '''
        Set a uniform onsite disorder. 

        :param alpha: Stength of the disorder.
        '''
        test_set_ons_disorder(self.ons, alpha)
        self.ons *= 1. + alpha * rand.uniform(-0.5, 0.5, self.lat.sites)
        self.alpha_on = alpha

    def get_coor_hop(self):
        '''
        Get the site coordinates in hopping space 
          considering just the nearest neighbors hoppings.
        '''
        visited = np.zeros(self.lat.sites, 'u2')
        self.coor_hop = np.zeros(self.lat.sites, dtype=[ ('x','f8'), ('y','f8'), ('tag','S1')])
        #self.dist_uni[1]
        tag_hop = np.unique(self.hop['tag'])
        dict_hop_vec = {}
        for tag in tag_hop:
            hop_find = self.hop[self.hop['tag']==tag][0]
            x = self.lat.coor['x'][hop_find['j']] - self.lat.coor['x'][hop_find['i']]
            y = self.lat.coor['y'][hop_find['j']] - self.lat.coor['y'][hop_find['i']]
            dict_hop_vec[tag] = (x, y)
        i_visit = 0
        while True:
            hs = self.hop[self.hop['i'] == i_visit]
            for h in hs:
                self.coor_hop['x'][h['j']] = self.coor_hop['x'][i_visit] + \
                    h['t'].real*dict_hop_vec[h['tag'].item()][0]
                self.coor_hop['y'][h['j']] = self.coor_hop['y'][i_visit] + \
                    h['t'].real*dict_hop_vec[h['tag'].item()][1]
                visited[h['j']] = 1
            visited[i_visit] = 2
            explored = np.argwhere(visited == 1)
            if not explored.any():
                break
            i_visit = explored[0]

    def get_ham(self, complex_transpose=False):
        '''
        Get the Tight-Binding Hamiltonian.

        :param compl_trans: Default value False. Add complex transposed part to the Hamiltonian.
        '''
        test_get_ham(self.hop, complex_transpose)
        self.ham = sparse.csr_matrix((self.hop['t'], (self.hop['i'], self.hop['j'])), 
                                                        shape=(self.lat.sites, self.lat.sites)) \
                       + sparse.diags(self.ons, 0)
        if complex_transpose:
            self.ham += sparse.csr_matrix((self.hop['t'].conj(), (self.hop['j'], self.hop['i'])), 
                                                        shape=(self.lat.sites, self.lat.sites))

    def get_eig(self, eigenvec=False):
        '''
        Get the eigenergies, eigenvectors and polarisations of the Tight-Binding model
        for non-Hermitian Hamiltonians.

        :param eigenvec: Default value False. Get the eigenvectors.
        '''
        test_get_eig(self.ham, eigenvec)
        if eigenvec:
            if (self.ham.H != self.ham).nnz:
                self.en, self.vn = LA.eig(self.ham.toarray())
            else:
                self.en, self.vn = LA.eigh(self.ham.toarray())
            ind = np.argsort(self.en.real)
            self.en = self.en[ind]
            self.vn = self.vn[:, ind]
            self.intensity = np.abs(self.vn) ** 2
            self.pola = np.zeros((self.lat.sites, len(self.lat.tags)))
            for i, t in enumerate(self.lat.tags):
                self.pola[:, i] = np.sum(np.abs(self.vn[self.lat.coor['tag'] == t, :]) ** 2, axis=0)
        else:
            if (self.ham.H != self.ham).nnz:
                self.en = LA.eigvals(self.ham.toarray())
                ind = np.argsort(self.en.real)
                self.en = self.en[ind]
            else:
                self.en = LA.eigvalsh(self.ham.toarray())

    def get_state_pola(self, tag_pola):
        '''
        Get the state with maximal polarization on one sublattice.

        :param tag: Sublattice tag.

        :returns:
            * **intensity** -- Intensity of max polarized state on *tag*.
        '''
        test_get_state_pola(self.vn, tag_pola, self.lat.tags)
        i_tag = self.lat.tags == tag_pola
        ind = np.argmax(self.pola[:, i_tag])
        print('State with polarization:', self.pola[ind, i_tag])
        return self.intensity[:, ind]

    def get_states_en(self, e_min, e_max):
        '''
        Get, if any, the intensity of the sum of the states 
        between *e_min* and *e_max*.

        :param e_min: Energy min.
        :param e_min: Energy min.
        :param e_max: Energy max.

        :returns:
            * **intensity** -- Sum of the intensities between *e_min* and *e_max*.
        '''
        test_get_states_en(self.vn, e_min, e_max)
        ind = np.where((self.en > e_min) & (self.en < e_max))
        ind = np.ravel(ind)
        print('{} states between {} and {}'.format(len(ind), e_min, e_max))
        intensity = np.sum(np.abs(self.vn[:, ind]) ** 2, axis=1)
        return intensity


'''
import matplotlib.pyplot as plt
from latticeTB import latticeTB
lat = latticeTB(ri=[[0, 0], [1, 0],  [0, 1]], tags=[b'a', b'b', b'c'], nor=2, ang=np.pi/2)       
lat.get_lattice(nx=8, ny=8)
#lat.plt_lattice()
eig = eigTB(lat)
eig.set_hop_nearest(dict_hop={b'ab':2, b'ba':1, b'ac':2, b'ca':1})
eig.set_dimerization_def(dict_hop={b'ab':1, b'ba':2}, x_bottom_left=8, y_bottom_left=0)
eig.set_dimerization_def(dict_hop={b'ac':1, b'ca':2}, x_bottom_left=0, y_bottom_left=8)
eig.get_coor_hop()
print(eig.coor_hop)
'''





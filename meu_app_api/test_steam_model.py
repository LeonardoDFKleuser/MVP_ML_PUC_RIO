#---------------------------------------------------------------- 
# Funções de teste
# ---------------------------------------------------------------

# Para iniciar o teste, digite o seguinte comando: pytest test_model.py

class  TestClass:

    def test_noe(self):
        """ Verifica se o dataset atende ao número total 
        mínimo de elementos para ser submetido a um modelo
        de Machine Learning.
        """
        
        from main_test_model import Dataset
        dataset = Dataset

        minimum_noe = dataset.getNoe()
        assert minimum_noe >= 200
        

    def test_pop(self):
        """
        Verifica se o dataset atende ao percentual mínimo de 
        resultados (outcomes) positivos para ser submetido a 
        um modelo de Machine Learning.
        """

        from main_test_model import Dataset
        dataset = Dataset

        minimum_pop = dataset.getPop()
        assert minimum_pop >= 0.05
        

class TestModel:

    def test_acc(self):
        """
        Verifica se o model atende ao valor de acurácia
        mínimo aceitável.
        """

        from main_test_model import TestModel
        my_model = TestModel

        minimum_acc = my_model.get_acc()

        assert minimum_acc >= 0.65

    def test_recall(self):
        """
        Verifica se o model atende ao valor
        mínimo aceitável para o requisito 'recall'.
        """

        from main_test_model import TestModel
        my_model = TestModel

        min_recall = my_model.get_recall()

        assert min_recall >= 0.5

    def test_precision(self):
        """
        Verifica se o model atende ao valor
        mínimo aceitável para o requisito 'precision'.
        """

        from main_test_model import TestModel
        my_model = TestModel

        min_precision = my_model.get_recall()

        assert min_precision >= 0.5
    
    def test_f1_score(self):
        """
        Verifica se o model atende ao valor
        mínimo aceitável para o requisito 'f1_score'.
        """

        from main_test_model import TestModel
        my_model = TestModel

        min_f1_score = my_model.get_recall()

        assert min_f1_score >= 0.5
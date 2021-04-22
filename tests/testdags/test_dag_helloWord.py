import unittest
from airflow.models import DagBag

class TestDagHelloWorld (unittest.TestCase):

    def setUp(self) -> None:
        self.dagbag = DagBag()

    def test_no_tasks (self):
        """
        the function test total number of tasks in the dag
        :return:
        """
        dag_id = "hello_world",
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 2)

    def test_contain_tasks(self):
        """Check task contains in hello_world dag"""
        dag_id = 'hello_world'
        dag = self.dagbag.get_dag(dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, ['dummy_task', 'hello_task'])

suite = unittest.TestLoader().loadTestsFromTestCase(TestDagHelloWorld)
unittest.TextTestRunner(verbosity=2).run(suite)
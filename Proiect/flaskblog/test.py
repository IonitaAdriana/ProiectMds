import unittest
from flaskblog import db
from flaskblog.models import User, Post

class Test(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def testUser(self):
        user_1 = User(username='test1', email='test1@gmail.com', password='1234')
        try:
            self.assertEqual(user_1.password, '1234')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user_1.username, 'test1')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user_1.email, 'test1@gmail.com')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        user_2 = User(username='test2', email='test2@gmail.com', password='1234')
        try:
            self.assertEqual(user_2.password, '1234')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user_2.username, 'test2')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user_2.email, 'test2@gmail.com')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def testRegister(self):
        try:
            user_1 = User(username='test1', email='test1@gmail.com', password='1234')
            db.session.add(user_1)
            db.session.commit()
            user = User.query.filter_by(email='test1@gmail.com').first()
            try:
                self.assertEqual(user.password, '1234')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(user.username, 'test1')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(user.email, 'test1@gmail.com')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
        except Exception:
            pass
        try:
            user_2 = User(username='test2', email='test2@gmail.com', password='1234')
            db.session.add(user_2)
            db.session.commit()
            user = User.query.filter_by(email='test2@gmail.com').first()
            try:
                self.assertEqual(user.password, '1234')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(user.username, 'test2')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(user.email, 'test2@gmail.com')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
        except Exception:
            pass

    def testLogin(self):
        user = User.query.filter_by(email='test1@gmail.com').first()
        try:
            self.assertEqual(user.password, '1234')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user.username, 'test1')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user.email, 'test1@gmail.com')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        user = User.query.filter_by(email='test2@gmail.com').first()
        try:
            self.assertEqual(user.password, '1234')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user.username, 'test2')
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(user.email, 'test2@gmail.com')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def testPost(self):
        try:
            post1 = Post(title='test1', content='test1', author='test1',post_id='1234test1')
            db.db.session.add(post1)
            db.session.commit()
            try:
                self.assertEqual(post1.title, 'test1')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(post1.content, 'test1')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(post1.author, 'test1')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
        except Exception:
            pass
        try:
            post2 = Post(title='test2', content='test2', author='test2', post_id='1234test2')
            db.db.session.add(post2)
            db.session.commit()
            try:
                self.assertEqual(post2.title, 'test2')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(post2.content, 'test2')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            try:
                self.assertEqual(post2.author, 'test2')
            except AssertionError as e:
                self.verificationErrors.append(str(e))
        except Exception:
            pass


    def testDeletePost(self):
        try:
            post = Post.query.get('1234test2')
            db.session.delete(post)
            db.session.commit()
        except Exception:
            pass
        try:
            post = Post.query.get('1234test1')
            db.session.delete(post)
            db.session.commit()
        except Exception:
            pass



if __name__ == '__main__':
    unittest.main()

{-# LANGUAGE DataKinds #-}
{-# LANGUAGE GADTs #-}
{-# LANGUAGE KindSignatures #-}

data DoorState = Opened | Closed | Locked
    deriving (Show, Eq)

data Door :: DoorState -> * where
    UnsafeMkDoor :: { material :: String } -> Door s
    deriving Show

closeDoor :: Door 'Opened -> Door 'Closed
closeDoor (UnsafeMkDoor m) = UnsafeMkDoor m

lockDoor :: Door 'Closed -> Door 'Locked
lockDoor (UnsafeMkDoor m) = UnsafeMkDoor m

openDoor :: Door 'Closed -> Door 'Opened
openDoor (UnsafeMkDoor m) = UnsafeMkDoor m

--doorStatus :: Door s -> DoorState
-- How do I implement this??

--mkDoor :: DoorState -> String -> Door s
-- Can I do this??
--mkDoor Opened m = UnsafeMkDoor m :: Door Opened
--mkDoor Closed m = UnsafeMkDoor m :: Door Opened
--mkDoor Locked m = UnsafeMkDoor m :: Door Opened


-- Enter singletons! A singleton is a type with exactly one value. 
-- The design pattern refers to a parametrized type that gives a
-- singleton type for each parameter. Like this:

data SingDS :: DoorState -> * where
    SOpened :: SingDS 'Opened
    SClosed :: SingDS 'Closed
    SLocked :: SingDS 'Locked

lockAnyDoor :: SingDS s -> Door s -> Door 'Locked
lockAnyDoor sng door = case sng of
    SOpened -> lockDoor (closeDoor door)
    SClosed -> lockDoor door
    SLocked -> door

doorStatus :: SingDS s -> Door s -> DoorState
doorStatus SOpened _ = Opened
doorStatus SClosed _ = Closed
doorStatus SLocked _ = Locked



class SingDSI s where
    singDS :: SingDS s

instance SingDSI 'Opened where
    singDS = SOpened
instance SingDSI 'Closed where
    singDS = SClosed
instance SingDSI 'Locked where
    singDS = SLocked

mkDoor :: SingDS s -> String -> Door s
mkDoor _ = UnsafeMkDoor
lockAnyDoor_ :: (SingDSI s) => Door s -> Door 'Locked
lockAnyDoor_ = lockAnyDoor singDS

doorStatus_ :: (SingDSI s) => Door s -> DoorState
doorStatus_ = doorStatus singDS


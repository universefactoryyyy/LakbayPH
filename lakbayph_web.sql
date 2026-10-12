-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 03, 2026 at 04:30 PM
-- Server version: 8.0.43
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lakbayph_web`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookingaddons`
--

CREATE TABLE `bookingaddons` (
  `BookingAddOnID` int NOT NULL,
  `BookingID` int NOT NULL,
  `AddOnID` int NOT NULL,
  `Quantity` int NOT NULL DEFAULT '1',
  `UnitPrice` decimal(10,2) NOT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `bookingamounts`
-- (See below for the actual view)
--
CREATE TABLE `bookingamounts` (
`AddOnTotal` decimal(42,2)
,`BaseAmount` decimal(20,2)
,`BookingID` int
,`BookingReference` varchar(20)
,`DiscountAmount` decimal(47,2)
,`DiscountPercentage` decimal(5,2)
,`FinalAmount` decimal(48,2)
,`NumberOfPeople` int
,`PackageID` int
,`PromoID` int
,`PromoTypeName` enum('PWD','SENIOR CITIZEN')
,`SubTotal` decimal(43,2)
,`UserID` int
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `bookingcompleteview`
-- (See below for the actual view)
--
CREATE TABLE `bookingcompleteview` (
`AddOnTotal` decimal(42,2)
,`BaseAmount` decimal(20,2)
,`BookingDate` timestamp
,`BookingID` int
,`BookingReference` varchar(20)
,`DiscountAmount` decimal(47,2)
,`DiscountPercentage` decimal(5,2)
,`Email` varchar(100)
,`EndDate` date
,`FinalAmount` decimal(48,2)
,`FirstName` varchar(50)
,`LastName` varchar(50)
,`NumberOfPeople` int
,`PackageID` int
,`PackageLocation` varchar(200)
,`PackageTitle` varchar(200)
,`PackageType` varchar(50)
,`PaymentDate` timestamp
,`PaymentMethod` varchar(20)
,`PaymentStatus` varchar(20)
,`Phone` varchar(20)
,`PromoTypeName` enum('PWD','SENIOR CITIZEN')
,`Status` varchar(20)
,`SubTotal` decimal(43,2)
,`TransactionReference` varchar(50)
,`TravelDate` date
,`UserID` int
);

-- --------------------------------------------------------

--
-- Table structure for table `bookinghistory`
--

CREATE TABLE `bookinghistory` (
  `HistoryID` int NOT NULL,
  `BookingID` int NOT NULL,
  `UserID` int NOT NULL,
  `ActionType` varchar(50) NOT NULL,
  `ActionDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ActionDescription` text,
  `PreviousStatus` varchar(20) DEFAULT NULL,
  `NewStatus` varchar(20) DEFAULT NULL,
  `ModifiedBy` int DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookingpackages`
--

CREATE TABLE `bookingpackages` (
  `BookingPackageID` int NOT NULL,
  `BookingID` int NOT NULL,
  `PackageID` int NOT NULL,
  `TravelDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `NumberOfPeople` int NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookingpayments`
--

CREATE TABLE `bookingpayments` (
  `BookingID` int NOT NULL,
  `PaymentMethod` varchar(20) NOT NULL DEFAULT 'Pay on Trip',
  `PaymentStatus` varchar(20) NOT NULL DEFAULT 'Pending',
  `PaymentDate` timestamp NULL DEFAULT NULL,
  `TransactionReference` varchar(50) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `BookingID` int NOT NULL,
  `BookingReference` varchar(20) NOT NULL,
  `UserID` int NOT NULL,
  `PackageID` int NOT NULL,
  `NumberOfPeople` int NOT NULL DEFAULT '1',
  `PromoID` int DEFAULT NULL,
  `TravelDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `BookingDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Status` varchar(20) NOT NULL DEFAULT 'Pending',
  `Notes` varchar(500) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `bookingwithreviewsview`
-- (See below for the actual view)
--
CREATE TABLE `bookingwithreviewsview` (
`AddOnTotal` decimal(42,2)
,`BaseAmount` decimal(20,2)
,`BookingDate` timestamp
,`BookingID` int
,`BookingReference` varchar(20)
,`CustomerName` varchar(101)
,`DiscountAmount` decimal(47,2)
,`Email` varchar(100)
,`EndDate` date
,`FinalAmount` decimal(48,2)
,`FirstName` varchar(50)
,`LastName` varchar(50)
,`NumberOfPeople` int
,`PackageID` int
,`PackageLocation` varchar(200)
,`PackageTitle` varchar(200)
,`PackageType` varchar(50)
,`PaymentDate` timestamp
,`PaymentMethod` varchar(20)
,`PaymentStatus` varchar(20)
,`Phone` varchar(20)
,`Rating` int
,`Status` varchar(20)
,`TransactionReference` varchar(50)
,`TravelDate` date
,`TripDuration` int
,`UserID` int
);

-- --------------------------------------------------------

--
-- Table structure for table `expensecategories`
--

CREATE TABLE `expensecategories` (
  `ExpenseCategoryID` int NOT NULL,
  `Category` varchar(100) NOT NULL,
  `CategoryType` enum('Startup','Operating') NOT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `expensecategories`
--

INSERT INTO `expensecategories` (`ExpenseCategoryID`, `Category`, `CategoryType`, `IsActive`, `CreatedAt`, `UpdatedAt`) VALUES
(1, 'Technology & Website', 'Operating', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(2, 'Content Creation & SEO', 'Operating', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(3, 'Business Operations', 'Operating', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(4, 'Legal & Compliance', 'Operating', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(5, 'Personal Development', 'Operating', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `ExpenseID` int NOT NULL,
  `ExpenseItem` varchar(100) NOT NULL,
  `ExpenseType` enum('Startup','Operating') NOT NULL,
  `ExpenseCategoryID` int NOT NULL,
  `BookingID` int DEFAULT NULL,
  `Amount` decimal(12,2) NOT NULL,
  `ExpenseDate` date NOT NULL,
  `PaymentMethod` varchar(50) DEFAULT NULL,
  `ReceiptNumber` varchar(100) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `RecordedBy` int DEFAULT NULL,
  `RecordedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `income`
--

CREATE TABLE `income` (
  `IncomeID` int NOT NULL,
  `IncomeItem` varchar(100) NOT NULL,
  `IncomeType` enum('Operating') NOT NULL,
  `IncomeSourceID` int NOT NULL,
  `BookingID` int DEFAULT NULL,
  `IncomeDate` date NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `RecordedBy` int DEFAULT NULL,
  `RecordedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `incomeamounts`
-- (See below for the actual view)
--
CREATE TABLE `incomeamounts` (
`BookingID` int
,`Description` varchar(255)
,`IncomeDate` date
,`IncomeID` int
,`IncomeItem` varchar(100)
,`IncomeSourceID` int
,`IncomeType` enum('Operating')
,`RecordedAt` timestamp
,`RecordedBy` int
);

-- --------------------------------------------------------

--
-- Table structure for table `incomesources`
--

CREATE TABLE `incomesources` (
  `IncomeSourceID` int NOT NULL,
  `Category` varchar(100) NOT NULL,
  `CommissionRate` varchar(20) DEFAULT NULL,
  `MonthlyMin` decimal(12,2) DEFAULT NULL,
  `MonthlyMax` decimal(12,2) DEFAULT NULL,
  `AnnualMin` decimal(12,2) DEFAULT NULL,
  `AnnualMax` decimal(12,2) DEFAULT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `incomesources`
--

INSERT INTO `incomesources` (`IncomeSourceID`, `Category`, `CommissionRate`, `MonthlyMin`, `MonthlyMax`, `AnnualMin`, `AnnualMax`, `IsActive`, `CreatedAt`, `UpdatedAt`) VALUES
(1, 'Freediving Tour Packages', '12-18%', 20000.00, 50000.00, 240000.00, 600000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(2, 'Domestic Tour Packages', '10-15%', 35000.00, 75000.00, 420000.00, 900000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(3, 'International Tour Packages', '8-12%', 25000.00, 60000.00, 300000.00, 720000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(4, 'Hotel Bookings', '8-10%', 15000.00, 30000.00, 180000.00, 360000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(5, 'Flight Bookings', '2-5%', 8000.00, 20000.00, 96000.00, 240000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(6, 'Transportation Services', '10-15%', 5000.00, 15000.00, 60000.00, 180000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(7, 'Travel Insurance', '15-25%', 3000.00, 8000.00, 36000.00, 96000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(8, 'Visa Processing Services', 'Fixed Fee', 5000.00, 12000.00, 60000.00, 144000.00, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Table structure for table `packageaddons`
--

CREATE TABLE `packageaddons` (
  `AddOnID` int NOT NULL,
  `PackageID` int NOT NULL,
  `AddOnName` varchar(200) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Unit` varchar(50) DEFAULT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `packageaddons`
--

INSERT INTO `packageaddons` (`AddOnID`, `PackageID`, `AddOnName`, `Price`, `Unit`, `IsActive`, `CreatedAt`) VALUES
(1, 1, 'Extra Fun Dive Session', 800.00, 'per session', 1, '2025-08-24 07:11:00'),
(2, 1, 'Underwater Photography Service', 1200.00, 'per session', 1, '2025-08-24 07:11:00'),
(3, 1, 'Equipment Rental (Full Set)', 500.00, 'per day', 1, '2025-08-24 07:11:00'),
(4, 2, 'Private Instructor', 1500.00, 'per day', 1, '2025-08-24 07:11:00'),
(5, 2, 'Room Upgrade to AC', 800.00, 'per night', 1, '2025-08-24 07:11:00'),
(6, 3, 'Romantic Dinner Setup', 2000.00, 'per couple', 1, '2025-08-24 07:11:00'),
(7, 3, 'Professional Photo Package', 1800.00, 'per session', 1, '2025-08-24 07:11:00'),
(8, 4, 'Additional Boat Dive', 1200.00, 'per dive', 1, '2025-08-24 07:11:00'),
(9, 4, 'Equipment Insurance', 300.00, 'per trip', 1, '2025-08-24 07:11:00'),
(10, 5, 'Private Boat Charter', 3000.00, 'per day', 1, '2025-08-24 07:11:00'),
(11, 5, 'Massage Therapy Session', 1000.00, 'per session', 1, '2025-08-24 07:11:00'),
(12, 13, 'Domestic Flight Upgrade', 5000.00, 'per person', 1, '2025-08-24 07:11:00'),
(13, 13, 'Hotel Room Upgrade', 2000.00, 'per night', 1, '2025-08-24 07:11:00'),
(14, 13, 'Extra Island Tour', 1500.00, 'per person', 1, '2025-08-24 07:11:00'),
(15, 14, 'ATV Rental', 800.00, 'per day', 1, '2025-08-24 07:11:00'),
(16, 14, 'Massage Service', 1200.00, 'per session', 1, '2025-08-24 07:11:00'),
(17, 25, 'Business Class Upgrade', 25000.00, 'per person', 1, '2025-08-24 07:11:00'),
(18, 25, '5-Star Hotel Upgrade', 8000.00, 'per night', 1, '2025-08-24 07:11:00'),
(19, 25, 'Private Tour Guide', 3000.00, 'per day', 1, '2025-08-24 07:11:00'),
(20, 26, 'Travel Insurance', 2500.00, 'per person', 1, '2025-08-24 07:11:00'),
(21, 26, 'Visa Processing Assistance', 1500.00, 'per person', 1, '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Stand-in structure for view `packageavailability`
-- (See below for the actual view)
--
CREATE TABLE `packageavailability` (
`AvailableSlots` decimal(33,0)
,`BookedSlots` decimal(32,0)
,`EndDate` date
,`IsActive` tinyint(1)
,`MaxSlots` int
,`PackageID` int
,`PackageType` varchar(50)
,`StartDate` date
,`Status` varchar(50)
,`Title` varchar(200)
);

-- --------------------------------------------------------

--
-- Table structure for table `packagedetails`
--

CREATE TABLE `packagedetails` (
  `PackageID` int NOT NULL,
  `PackageType` enum('Freediving','Domestic','International') NOT NULL,
  `FlagSymbol` varchar(10) DEFAULT NULL,
  `IdealFor` varchar(255) DEFAULT NULL,
  `Inclusions` text,
  `ImageFileName` varchar(50) DEFAULT NULL,
  `Highlights` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `packagedetails`
--

INSERT INTO `packagedetails` (`PackageID`, `PackageType`, `FlagSymbol`, `IdealFor`, `Inclusions`, `ImageFileName`, `Highlights`) VALUES
(1, 'Freediving', '🏊‍♀️', 'Beginners and non-divers', 'Day Tour Class (Open Water) training, 1 Fun Dive session with certified instructors, Access to DOT ACCREDITED Accommodation (Private AC Room), Access to resort amenities (lounge areas, showers), Light breakfast and local lunch', 'fdbasic.jpg', 'Perfect for first-timers and those short on time!'),
(2, 'Freediving', '🌅', 'Couples and sunset lovers', 'Sunset Fun Dive session with certified instructors, Resort access with sunset viewing deck, Welcome drinks and light snacks, Photo souvenir and underwater shots, Optional romantic dinner package', 'fdsunset.jpg', 'A romantic and peaceful dive at golden hour.'),
(3, 'Freediving', '🌌', 'Adventurers and photographers', 'Night Fun Dive with underwater light guides, Instructor-led safety orientation, Night snacks and hot drinks, Photo and video coverage, Resort amenities (lounge, rinse area)', 'fdnight.jpg', 'Witness bioluminescent plankton in a serene night dive.'),
(4, 'Freediving', '🤿', 'Beginners who want to explore more or divers seeking intensive experience', '2 Days 1 Night Class (Open Water) certification, 2 Fun Dive sessions with certified instructors, 1 Boat Dive experience with certified instructors, Island Hopping tour, Cabin Room Accommodation (Fan Room), All meals included, Access to resort amenities', 'fd2days.jpg', 'For those looking to go a bit deeper into the diving experience!'),
(5, 'Freediving', '🏝️', 'Intermediate divers looking for mix of adventure and relaxation', '1 Fun Dive session with certified instructors, 2 Boat Dive experiences with certified instructors, Island Hopping tour, Access to City Pool Dive for skill practice, DOT ACCREDITED Accommodation (Private AC Room), All meals included', 'fdisland.jpg', 'Combine a diving adventure with a scenic island escape!'),
(6, 'Freediving', '⚔️', 'Weekend travelers and active divers', '2 Boat Dive sessions at top Puerto Galera sites, 1 Night Dive experience, Cabin Room Accommodation (Fan), All meals included, Speedboat transportation', 'fdwarrior.jpg', 'Maximize your weekend with action-packed dives!'),
(7, 'Freediving', '🏆', 'Aspiring freedivers or those looking to advance freediving skills', 'Molchanov\'s Certification Course (Wave 1 or Wave 2), Basic and Advanced Line Training, Pool training and skill sessions at City Pool Dive, Island Hopping activity on rest days, DOT ACCREDITED Accommodation (Private AC Room), All meals and training materials included', 'fdtrain.jpg', 'Ideal for divers looking to become certified freedivers!'),
(8, 'Freediving', '🎓', 'Experienced divers aiming to go pro', 'Advanced depth and static apnea training, Instructor mentorship and evaluations, Night dive and rescue scenarios, Training logbooks and certification, Camp-style shared accommodation', 'fdmaster.jpg', 'Push your limits with elite training and mentorship.'),
(9, 'Freediving', '👨‍👩‍👧‍👦', 'Families and friends seeking memorable experience together', 'Choice of Fun Dive or Mermaid Tail Dive per person, Pool Training session for beginners, Boat Dive to top dive sites in Mabini, Island Hopping tour, DOT ACCREDITED Accommodation (AC or Cabin Room), All meals included, Mermaid tails provided if selected', 'fdfam.jpg', 'The perfect package for groups to enjoy relaxed diving and island getaway!'),
(10, 'Freediving', '🧘‍♀️', 'Relaxation seekers and wellness enthusiasts', 'Daily yoga and breathwork sessions, Pool and line training dives, Beachside meditation and bonfire, Vegetarian wellness meals, Beachfront hut accommodation', 'fdyoga.jpg', 'Balance breath, body, and sea in this holistic retreat.'),
(11, 'Freediving', '📸', 'Photography enthusiasts and creative divers', '2 Guided underwater photo dives, Camera gear rental (optional), Photography workshop session, Accommodation with editing station access, Meal plan and island tour', 'fdphoto.jpg', 'Capture marine beauty through your lens.'),
(12, 'Freediving', '💑', 'Couples looking for romance and adventure', 'Couples dive session with instructor, Private beachfront dinner setup, 1 Night AC Room Accommodation, Breakfast and sunset cocktails, Photo souvenir and dive certificate', 'fdcouples.jpg', 'Dive together and enjoy a beachfront dinner under the stars.'),
(13, 'Domestic', '🏝️', 'Beach lovers and adventure seekers', 'Round-trip flights Manila-Puerto Princesa-Manila, 5 nights accommodation (2 nights Puerto Princesa, 3 nights El Nido), Daily breakfast and 3 seafood dinners, Airport transfers and land transportation, Underground River tour with permits, El Nido island hopping tours A & C, Snorkeling equipment and boat transfers, Environmental and entrance fees', 'dompalawan.jpg', 'UNESCO World Heritage Underground River, Big Lagoon and Small Lagoon in El Nido, Seven Commando Beach and Helicopter Island, Pristine white sand beaches, Crystal clear turquoise waters'),
(14, 'Domestic', '🏖️', 'Party-goers and beach enthusiasts', 'Round-trip flights Manila-Kalibo-Manila, 3 nights accommodation beachfront hotel, Daily breakfast and sunset dinner cruise, Airport transfers and boat transfers to island, Island hopping with snorkeling, Sunset sailing and paraw boat experience, ATV adventure and helmet zorbing, White Beach access and activities', 'domboracay.png', '4-kilometer stretch of powdery White Beach, Vibrant nightlife and beach parties, Water sports: parasailing, jet skiing, diving, Stunning Boracay sunsets, Fresh seafood and tropical dining'),
(15, 'Domestic', '🏄‍♂️', 'Surfers and island hoppers', 'Round-trip flights Manila-Sayak Airport-Manila, 4 nights accommodation in General Luna, Daily breakfast and 2 local dinners, Airport transfers and motorcycle rentals, Surf lessons at Cloud 9 with board rental, Island hopping to Naked, Daku, and Guyam Islands, Magpupungko Rock Pools natural jacuzzi tour, Coconut and palm tree climbing experience', 'domsiargao.jpg', 'World-renowned Cloud 9 surfing break, Crystal clear Magpupungko Rock Pools, Pristine uninhabited islands, Laid-back island lifestyle, Fresh coconuts and tropical island vibes'),
(16, 'Domestic', '⚓', 'Scuba divers and underwater adventurers', 'Round-trip flights Manila-Busuanga-Manila, 4 nights dive resort accommodation, Daily breakfast and 3 dive days, 2 shipwreck dives + 1 coral garden dive per day, All dive gear rental included, Island hopping: Kayangan Lake, Twin Lagoon, BBQ lunch on beach picnic', 'domcoron.jpg', 'WWII Japanese shipwreck dives, Clear waters of Kayangan Lake, Stunning coral gardens, Thermal hot spring soaking, Dramatic limestone cliffs and lagoons'),
(17, 'Domestic', '🌋', 'Nature lovers and outdoor explorers', 'Round-trip flights Manila-Cagayan de Oro-Manila, 3 nights accommodation in Camiguin eco-lodge, Daily breakfast and welcome dinner, Ferry transfer to Camiguin, White Island sandbar tour, Tuasan and Katibawasan Falls trek, Sunken Cemetery snorkeling, Ardent Hot Spring and Giant Clam Sanctuary', 'domcamiguin.jpg', 'Volcanic hot springs and waterfalls, Crystal clear waters and marine life, Historical Sunken Cemetery dive site, Charming small-island vibe, Majestic Mt. Hibok-Hibok'),
(18, 'Domestic', '🏕️', 'Quick getaways and campers', 'Private van transport from Manila (round-trip), Boat transfers to Anawangin, Nagsasa, and Capones Islands, 2 nights tent accommodation with camp gear, All meals during the tour (6 total), Bonfire night and stargazing activity, Entrance and environmental fees, Local guide and safety orientation', 'domzambales.jpg', 'Secluded white sand coves, Camping by the beach with bonfires, Trekking and photo ops at Capones Lighthouse, Lush pine tree surroundings, Unplugged escape from the city'),
(19, 'Domestic', '🌄', 'Families and nature enthusiasts', 'Round-trip flights Manila-Tagbilaran-Manila, 3 nights accommodation in Panglao Island resort, Daily breakfast and welcome dinner, Airport transfers and tour transportation, Chocolate Hills viewing and Carmen tour, Tarsier Sanctuary visit, Loboc River cruise with lunch, Baclayon Church and Blood Compact Monument', 'dombohol.png', '1,776 geological formations of Chocolate Hills, World\'s smallest primate - Philippine Tarsier, Scenic Loboc River floating restaurant, Beautiful Alona Beach in Panglao, Historic Baclayon Stone Church'),
(20, 'Domestic', '🌾', 'Culture seekers and hikers', 'Round-trip bus Manila-Baguio with sleeper accommodation, 4 nights accommodation (2 nights Banaue, 2 nights Baguio), Daily breakfast and traditional Cordillera meals, Land transfers and jeepney rides to viewpoints, Guided trek to Batad Rice Terraces, Sagada Hanging Coffins and Echo Valley tour, Baguio city tour: Burnham Park, Session Road, Strawberry picking in La Trinidad', 'dombanaue.jpg', 'UNESCO World Heritage Rice Terraces, 2000-year-old Ifugao engineering marvel, Mystical hanging coffins of Sagada, Cool mountain climate and pine forests, Indigenous Cordillera culture and traditions'),
(21, 'Domestic', '🐋', 'History buffs and marine life enthusiasts', 'Round-trip flights Manila-Cebu-Manila, 5 nights accommodation (2 nights Cebu City, 3 nights southern Cebu), Daily breakfast and heritage dinners, Airport transfers and southern Cebu van transfers, Whale shark swimming experience in Oslob, Cebu Heritage Monument and Magellan\'s Cross tour, Siquijor mystical island day trip, Moalboal sardine run and turtle watching', 'domcebu.jpg', 'Swimming with gentle whale sharks, Birthplace of Christianity in Asia, Historic Fort San Pedro and Basilica del Santo Niño, Millions of sardines underwater tornado, Sea turtle encounters in Moalboal'),
(22, 'Domestic', '🏛️', 'History lovers and road trippers', 'Private van transport from Manila (round-trip), 4 nights accommodation (1 Vigan, 2 Laoag, 1 Pagudpud), Daily breakfast and 2 local Ilocano meals, Vigan Heritage Village walking tour, Pagudpud beach hopping (Blue Lagoon, Saud Beach), Visit Paoay Church, Cape Bojeador Lighthouse, Sand dunes 4x4 ride and sandboarding experience', 'domilocos.jpg', 'UNESCO World Heritage Vigan, Paoay Church - Baroque architecture, Pagudpud\'s scenic beaches, Thrilling La Paz sand dunes adventure, Calle Crisologo\'s old-world charm'),
(23, 'Domestic', '🌿', 'Eco-tourists and thrill-seekers', 'Round-trip flights Manila-Davao-Manila, 4 nights accommodation (2 in Davao City, 2 in Samal Island), Daily breakfast and local cuisine lunch, Visit Philippine Eagle Center and Malagos Garden, Eden Nature Park zipline and sky cycling, Island hopping: Talicud Island, Coral Garden, Durian farm visit and city cultural tour', 'domdavao.jpg', 'Meet the endangered Philippine Eagle, Sky cycling over Davao forests, Tropical beaches and snorkeling in Samal, Durian and pomelo farms, Cultural immersion and eco-learning'),
(24, 'Domestic', '🌋🦈', 'Wildlife lovers and volcano trekkers', 'Round-trip flights Manila-Legazpi-Manila, 4 nights accommodation (2 Legazpi, 2 Donsol), Daily breakfast and Bicolano spicy dinner feast, Mt. Mayon ATV adventure trail ride, Whale shark interaction tour (seasonal), Cagsawa Ruins historical walking tour, Firefly river cruise and cultural dance show', 'dombicol.jpg', 'Perfect cone shape of Mayon Volcano, Gentle whale shark encounters in Donsol, Historic Cagsawa Church Ruins, Fiery Bicol cuisine experience, Evening firefly watching cruise'),
(25, 'International', '🏯', 'Culture enthusiasts and first-time visitors to Japan', 'Round-trip flights Manila-Tokyo, 6 nights accommodation in 4-star hotels, Daily breakfast and 3 authentic Japanese dinners, High-speed rail pass (JR Pass) for intercity travel, Guided tours of temples, shrines, and cultural sites, Visit to Mount Fuji and Hakone, Traditional tea ceremony experience, English-speaking tour guide', 'inttokyo.png', 'Cherry blossom viewing (seasonal), Shibuya Crossing and Tokyo Skytree, Fushimi Inari Shrine in Kyoto, Osaka Castle and Dotonbori district, Traditional ryokan stay experience'),
(26, 'International', '🛕', 'Beach lovers and adventure seekers', 'Round-trip flights Manila-Bangkok, 5 nights accommodation (2 nights Bangkok, 3 nights Phuket), Daily breakfast and welcome dinner, Airport transfers and inter-city transportation, Island hopping tour to Phi Phi Islands, Bangkok city tour including Grand Palace, Thai massage session, Snorkeling equipment and boat transfers', 'intbangkok.png', 'Maya Bay (The Beach movie location), Floating markets of Bangkok, Patong Beach nightlife, Traditional longtail boat rides, Authentic Thai street food tours'),
(27, 'International', '🦁', 'Families and urban explorers', 'Round-trip flights Manila-Singapore, 3 nights accommodation in Marina Bay area, Daily breakfast and 2 dinners, Airport transfers and MRT day passes, Gardens by the Bay admission, Universal Studios Singapore tickets, Singapore Zoo or Night Safari, City tour including Merlion and Chinatown', 'intsingapore.jpg', 'Marina Bay Sands SkyPark, Supertree Grove light show, Sentosa Island activities, Hawker center food tours, Clarke Quay riverside dining'),
(28, 'International', '🎎', 'K-pop fans and culture enthusiasts', 'Round-trip flights Manila-Seoul, 5 nights accommodation in Myeongdong area, Daily breakfast and Korean BBQ dinners, KTX high-speed train to Busan, Gyeongbokgung Palace and Bukchon Hanok Village, Jeju Island day trip (optional), K-beauty shopping tour in Hongdae, Traditional hanbok rental experience', 'intkorea.jpg', 'Gangnam district and Han River, Busan\'s colorful Gamcheon Village, N Seoul Tower and Lotte World, Korean spa (jjimjilbang) experience, Street food tours in Myeongdong'),
(29, 'International', '🏮', 'History buffs and nature lovers', 'Round-trip flights Manila-Hanoi, 7 nights accommodation in heritage hotels, Daily breakfast and traditional Vietnamese meals, Domestic flights Hanoi-Ho Chi Minh City, Ha Long Bay overnight cruise, Cu Chi Tunnels and War Remnants Museum, Mekong Delta day tour, Motorbike street food tour in Ho Chi Minh', 'intvietnam.jpg', 'UNESCO World Heritage Ha Long Bay, Ancient temples and French colonial architecture, Traditional water puppet shows, Floating markets of Mekong Delta, Authentic pho and banh mi experiences'),
(30, 'International', '🕌', 'Luxury travelers and shopping enthusiasts', 'Round-trip flights Manila-Dubai, 4 nights accommodation in 5-star hotel, Daily breakfast and farewell dinner, Private airport transfers in luxury vehicles, Burj Khalifa At The Top tickets, Desert safari with BBQ dinner, Dubai Mall and Gold Souk shopping tours, Abu Dhabi city tour including Sheikh Zayed Mosque', 'intdubai.jpg', 'Burj Al Arab and Palm Jumeirah, Dubai Fountain show and marina cruise, Traditional souks and spice markets, Luxury shopping in world\'s largest mall, Atlantis Aquaventure waterpark'),
(31, 'International', '🗼', 'Couples and art enthusiasts', 'Round-trip flights Manila-Paris, 5 nights accommodation in boutique hotel near Champs-Élysées, Daily breakfast and 2 romantic dinners, Airport transfers and Metro passes, Skip-the-line Eiffel Tower and Louvre tickets, Seine River cruise with dinner, Day trip to Palace of Versailles, Wine tasting in Montmartre', 'intparis.jpg', 'Iconic Eiffel Tower views, Mona Lisa at the Louvre Museum, Notre-Dame Cathedral and Sainte-Chapelle, Romantic stroll along the Seine, Authentic French café culture'),
(32, 'International', '🗽', 'City lovers and Broadway fans', 'Round-trip flights Manila-New York, 5 nights accommodation in Times Square area, Daily breakfast and 2 dinners, Airport transfers and MetroCard passes, Statue of Liberty and Ellis Island ferry, Broadway show tickets, Empire State Building observation deck, Central Park horse carriage ride', 'intnewyork.jpeg', 'Times Square neon lights, 9/11 Memorial and One World Observatory, Brooklyn Bridge and High Line walks, Metropolitan Museum of Art, Fifth Avenue luxury shopping'),
(33, 'International', '🏰', 'History lovers and royal enthusiasts', 'Round-trip flights Manila-London, 6 nights accommodation near Hyde Park, Daily breakfast and traditional pub dinner, Oyster Card for unlimited transport, Buckingham Palace and Windsor Castle tours, Thames River cruise, Day trip to Stonehenge and Bath, West End musical show', 'intlondon.jpg', 'Changing of the Guard ceremony, Tower of London and Crown Jewels, Big Ben and Westminster Abbey, British Museum treasures, Traditional afternoon tea experience'),
(34, 'International', '🏛️', 'Art lovers and foodies', 'Round-trip flights Manila-Rome, 8 nights accommodation in central hotels, Daily breakfast and 4 gourmet dinners, Vatican and Colosseum skip-the-line tickets, Train transfers between cities, Gondola ride in Venice, Cooking class in Florence, Walking tour of ancient Rome', 'intitaly.jpg', 'Trevi Fountain and Spanish Steps, Leaning Tower of Pisa (optional trip), Uffizi Gallery and Renaissance art, St. Peter\'s Basilica and Sistine Chapel, Venetian canals and Rialto Bridge'),
(35, 'International', '🎭', 'Nature lovers and beach enthusiasts', 'Round-trip flights Manila-Sydney, 6 nights accommodation with harbor views, Daily breakfast and farewell dinner, Airport transfers and Opal Card, Sydney Opera House guided tour, Blue Mountains day trip with wildlife park, Bondi Beach surfing lesson, Harbor Bridge climb experience', 'intsydney.jpg', 'Iconic Opera House performances, Sydney Harbour Bridge panoramic views, Bondi to Coogee coastal walk, Taronga Zoo with harbor backdrop, The Rocks historic area exploration'),
(36, 'International', '🍁', 'Nature photographers and adventure seekers', 'Round-trip flights Manila-Calgary, 6 nights lodge accommodation, Daily breakfast and 2 campfire dinners, Banff and Jasper National Park entry, Glacier Skywalk and Columbia Icefield tour, Wildlife watching in Jasper, Lake Louise canoe rental, Scenic drive along Icefields Parkway', 'intcanada.jpg', 'Snow-capped peaks and turquoise lakes, Moraine Lake and Lake Louise, Athabasca Glacier walking tour, Elk and bear sightings, Stargazing in Jasper\'s dark sky preserve');

-- --------------------------------------------------------

--
-- Table structure for table `packagelocations`
--

CREATE TABLE `packagelocations` (
  `PackageID` int NOT NULL,
  `Location` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `packagelocations`
--

INSERT INTO `packagelocations` (`PackageID`, `Location`) VALUES
(1, 'DOT Accredited Resort'),
(2, 'Batangas Sunset Bay'),
(3, 'Secret Bay, Batangas'),
(4, 'Freediving Resort'),
(5, 'Mabini Diving Sites'),
(6, 'Puerto Galera'),
(7, 'Certified Training Center'),
(8, 'Advanced Dive Camp'),
(9, 'Family-Friendly Resort'),
(10, 'Mindoro Wellness Resort'),
(11, 'Anilao Marine Sanctuary'),
(12, 'Private Resort, Batangas'),
(13, 'El Nido, Coron, Puerto Princesa'),
(14, 'Boracay Island, Aklan'),
(15, 'General Luna, Cloud 9, Magpupungko'),
(16, 'Coron, Palawan'),
(17, 'Camiguin Island'),
(18, 'Subic, Anawangin, Nagsasa, Capones'),
(19, 'Tagbilaran, Panglao, Chocolate Hills'),
(20, 'Banaue, Batad, Sagada, Baguio'),
(21, 'Cebu City, Oslob, Siquijor, Moalboal'),
(22, 'Vigan, Laoag, Pagudpud'),
(23, 'Davao City, Samal Island, Eden Park'),
(24, 'Legazpi, Donsol, Cagsawa Ruins'),
(25, 'Tokyo, Kyoto, Osaka'),
(26, 'Bangkok, Phuket, Phi Phi Islands'),
(27, 'Singapore'),
(28, 'Seoul, Busan'),
(29, 'Hanoi, Ha Long Bay, Ho Chi Minh'),
(30, 'Dubai, Abu Dhabi'),
(31, 'Paris, France'),
(32, 'New York, USA'),
(33, 'London, UK'),
(34, 'Rome, Florence, Venice'),
(35, 'Sydney, Australia'),
(36, 'Banff, Jasper, Lake Louise');

-- --------------------------------------------------------

--
-- Table structure for table `promodiscounts`
--

CREATE TABLE `promodiscounts` (
  `PromoID` int NOT NULL,
  `UserID` int NOT NULL,
  `PromoTypeID` int NOT NULL,
  `DocumentNumber` varchar(100) NOT NULL,
  `Status` enum('Pending','Approved','Rejected') NOT NULL DEFAULT 'Pending',
  `ValidatedBy` int DEFAULT NULL,
  `ValidationDate` timestamp NULL DEFAULT NULL,
  `ExpiryDate` date DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `promotypes`
--

CREATE TABLE `promotypes` (
  `PromoTypeID` int NOT NULL,
  `PromoTypeName` enum('PWD','SENIOR CITIZEN') NOT NULL,
  `DiscountPercentage` decimal(5,2) NOT NULL DEFAULT '20.00',
  `Description` varchar(255) DEFAULT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `promotypes`
--

INSERT INTO `promotypes` (`PromoTypeID`, `PromoTypeName`, `DiscountPercentage`, `Description`, `IsActive`, `CreatedAt`) VALUES
(1, 'PWD', 20.00, 'Person with Disability discount as per RA 7277', 1, '2025-08-24 07:11:00'),
(2, 'SENIOR CITIZEN', 20.00, 'Senior Citizen discount as per RA 9994', 1, '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Stand-in structure for view `recenttransactions`
-- (See below for the actual view)
--
CREATE TABLE `recenttransactions` (
`AdminName` varchar(101)
,`Amount` decimal(48,2)
,`BookingDate` timestamp
,`BookingID` int
,`Date` date
,`Description` varchar(255)
,`ExpenseCategory` varchar(100)
,`ExpenseItem` varchar(100)
,`IsIncome` bigint
,`PackageCategory` varchar(50)
,`PaymentMethod` varchar(50)
,`ReceiptNumber` varchar(100)
,`Type` varchar(7)
,`UserID` int
);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `ReviewID` int NOT NULL,
  `UserID` int NOT NULL,
  `BookingID` int DEFAULT NULL,
  `PackageID` int DEFAULT NULL,
  `Rating` int NOT NULL,
  `Comment` text,
  `ReviewDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `reviewstatistics`
-- (See below for the actual view)
--
CREATE TABLE `reviewstatistics` (
`AverageRating` decimal(13,2)
,`FiveStarCount` bigint
,`FiveStarPercentage` decimal(26,2)
,`FourStarCount` bigint
,`FourStarPercentage` decimal(26,2)
,`OneStarCount` bigint
,`OneStarPercentage` decimal(26,2)
,`ReviewsWithComments` bigint
,`ReviewsWithoutComments` bigint
,`ThreeStarCount` bigint
,`ThreeStarPercentage` decimal(26,2)
,`TotalReviews` bigint
,`TwoStarCount` bigint
,`TwoStarPercentage` decimal(26,2)
);

-- --------------------------------------------------------

--
-- Table structure for table `tourcategories`
--

CREATE TABLE `tourcategories` (
  `CategoryID` int NOT NULL,
  `CategoryName` varchar(100) NOT NULL,
  `CategoryType` varchar(50) NOT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tourcategories`
--

INSERT INTO `tourcategories` (`CategoryID`, `CategoryName`, `CategoryType`, `IsActive`, `CreatedAt`) VALUES
(1, 'Basic Training', 'Freediving', 1, '2025-08-24 07:11:00'),
(2, 'Certification Courses', 'Freediving', 1, '2025-08-24 07:11:00'),
(3, 'Adventure Packages', 'Freediving', 1, '2025-08-24 07:11:00'),
(4, 'Specialty Experiences', 'Freediving', 1, '2025-08-24 07:11:00'),
(5, 'Island Paradise', 'Domestic', 1, '2025-08-24 07:11:00'),
(6, 'Cultural Heritage', 'Domestic', 1, '2025-08-24 07:11:00'),
(7, 'Nature & Adventure', 'Domestic', 1, '2025-08-24 07:11:00'),
(8, 'Beach & Diving', 'Domestic', 1, '2025-08-24 07:11:00'),
(9, 'Asian Discovery', 'International', 1, '2025-08-24 07:11:00'),
(10, 'Western Culture', 'International', 1, '2025-08-24 07:11:00'),
(11, 'Luxury Destinations', 'International', 1, '2025-08-24 07:11:00'),
(12, 'Adventure Expeditions', 'International', 1, '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Table structure for table `tourpackages`
--

CREATE TABLE `tourpackages` (
  `PackageID` int NOT NULL,
  `Title` varchar(200) NOT NULL,
  `PackageType` varchar(50) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `Duration` int NOT NULL,
  `DurationNights` int NOT NULL DEFAULT '0',
  `CategoryID` int NOT NULL,
  `MaxSlots` int NOT NULL DEFAULT '10',
  `Status` varchar(50) DEFAULT 'active',
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `IsGroupPackage` tinyint(1) NOT NULL DEFAULT '0',
  `GroupSize` int DEFAULT '1',
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tourpackages`
--

INSERT INTO `tourpackages` (`PackageID`, `Title`, `PackageType`, `Price`, `Description`, `Duration`, `DurationNights`, `CategoryID`, `MaxSlots`, `Status`, `StartDate`, `EndDate`, `IsGroupPackage`, `GroupSize`, `IsActive`, `CreatedAt`, `UpdatedAt`) VALUES
(1, 'Basic Day Tour Dive', 'Freediving', 2500.00, 'Perfect for first-timers and those short on time!', 1, 0, 1, 15, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(2, 'Sunset Dive Experience', 'Freediving', 2800.00, 'A romantic and peaceful dive at golden hour.', 1, 0, 1, 12, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(3, 'Night Glow Dive Adventure', 'Freediving', 3200.00, 'Witness bioluminescent plankton in a serene night dive.', 1, 0, 4, 10, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(4, '2 Days 1 Night Open Water Package', 'Freediving', 6500.00, 'For those looking to go a bit deeper into the diving experience!', 2, 1, 1, 20, 'active', '2025-08-01', '2025-12-31', 1, 10, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(5, 'Adventure Dive & Island Hopping Package', 'Freediving', 7500.00, 'Combine a diving adventure with a scenic island escape!', 2, 1, 3, 16, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(6, 'Weekend Warrior Dive', 'Freediving', 7000.00, 'Maximize your weekend with action-packed dives!', 2, 1, 3, 14, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(7, 'Freediving Training & Certification', 'Freediving', 10000.00, 'Ideal for divers looking to become certified freedivers!', 3, 2, 2, 12, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(8, 'Master Diver Elite Course', 'Freediving', 18000.00, 'Push your limits with elite training and mentorship.', 5, 4, 2, 8, 'active', '2025-08-01', '2025-12-31', 1, 4, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(9, 'Family & Friends Ocean Retreat Package', 'Freediving', 12000.00, 'The perfect package for groups to enjoy relaxed diving and island getaway!', 3, 2, 4, 20, 'active', '2025-08-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(10, 'Freediving & Yoga Wellness Retreat', 'Freediving', 10500.00, 'Balance breath, body, and sea in this holistic retreat.', 3, 2, 4, 15, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(11, 'Underwater Photography Dive', 'Freediving', 8500.00, 'Capture marine beauty through your lens.', 2, 1, 4, 10, 'active', '2025-08-01', '2025-12-31', 1, 6, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(12, 'Couples Dive & Dine Getaway', 'Freediving', 9500.00, 'Dive together and enjoy a beachfront dinner under the stars.', 2, 1, 4, 8, 'active', '2025-08-01', '2025-12-31', 1, 2, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(13, 'Palawan Paradise Explorer', 'Domestic', 28000.00, 'Discover the pristine beauty of Palawan\'s world-class beaches!', 6, 5, 5, 25, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(14, 'Boracay Beach Bliss', 'Domestic', 22000.00, 'Experience the famous white sand beaches of Boracay.', 4, 3, 5, 30, 'active', '2025-08-01', '2025-12-31', 1, 20, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(15, 'Siargao Surf & Island Life', 'Domestic', 25000.00, 'Surf, relax, and enjoy island life in Siargao.', 5, 4, 5, 20, 'active', '2025-08-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(16, 'Coron Shipwreck Dive Adventure', 'Domestic', 27000.00, 'Explore WWII shipwrecks in Coron\'s crystal clear waters.', 5, 4, 8, 16, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(17, 'Camiguin Volcano & Waterfall Escape', 'Domestic', 16500.00, 'Discover the natural wonders of Camiguin Island.', 4, 3, 7, 18, 'active', '2025-08-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(18, 'Zambales Island Hopping Getaway', 'Domestic', 13500.00, 'Enjoy secluded beaches and island hopping in Zambales.', 3, 2, 5, 24, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(19, 'Bohol Heritage Adventure', 'Domestic', 18500.00, 'Explore the cultural and natural wonders of Bohol.', 4, 3, 6, 25, 'active', '2025-08-01', '2025-12-31', 1, 20, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(20, 'Banaue Rice Terraces Cultural Journey', 'Domestic', 19500.00, 'Witness the breathtaking rice terraces of Banaue.', 5, 4, 6, 20, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(21, 'Cebu Heritage & Island Discovery', 'Domestic', 24500.00, 'Experience the best of Cebu\'s heritage and islands.', 6, 5, 6, 22, 'active', '2025-08-01', '2025-12-31', 1, 18, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(22, 'Ilocos Historic Road Trip', 'Domestic', 18500.00, 'Travel through history in the Ilocos region.', 5, 4, 6, 20, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(23, 'Davao Eco Adventure Tour', 'Domestic', 21000.00, 'Experience Davao\'s natural wonders and wildlife.', 5, 4, 7, 18, 'active', '2025-08-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(24, 'Bicol Mayon & Whale Shark Expedition', 'Domestic', 23000.00, 'See Mayon Volcano and swim with whale sharks.', 5, 4, 7, 16, 'active', '2025-08-01', '2025-12-31', 1, 10, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(25, 'Japan Cultural Discovery', 'International', 85000.00, 'Experience the rich culture and traditions of Japan.', 7, 6, 9, 20, 'active', '2025-09-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(26, 'Thailand Beach Paradise', 'International', 45000.00, 'Relax on Thailand\'s beautiful beaches and islands.', 6, 5, 9, 25, 'active', '2025-08-01', '2025-12-31', 1, 20, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(27, 'Singapore City Explorer', 'International', 38000.00, 'Discover the modern marvels of Singapore.', 4, 3, 9, 20, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(28, 'South Korea K-Culture Tour', 'International', 65000.00, 'Immerse yourself in Korean culture and pop culture.', 6, 5, 9, 18, 'active', '2025-08-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(29, 'Vietnam Heritage Discovery', 'International', 52000.00, 'Explore Vietnam\'s rich history and natural beauty.', 8, 7, 9, 22, 'active', '2025-08-01', '2025-12-31', 1, 18, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(30, 'Dubai Luxury Experience', 'International', 95000.00, 'Experience the luxury and opulence of Dubai.', 5, 4, 11, 12, 'active', '2025-08-01', '2025-12-31', 1, 10, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(31, 'Paris Romance & Culture', 'International', 78000.00, 'Fall in love with the romance of Paris.', 6, 5, 10, 15, 'active', '2025-09-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(32, 'New York Big Apple Experience', 'International', 125000.00, 'Experience the energy of New York City.', 6, 5, 10, 12, 'active', '2025-09-01', '2025-12-31', 1, 10, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(33, 'London Royal Heritage Tour', 'International', 88000.00, 'Discover the royal history of London.', 7, 6, 10, 15, 'active', '2025-09-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(34, 'Italy Grand Tour', 'International', 99000.00, 'Experience the art, history, and cuisine of Italy.', 9, 8, 10, 18, 'active', '2025-09-01', '2025-12-31', 1, 15, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(35, 'Sydney Harbor Adventure', 'International', 105000.00, 'Explore the iconic sights of Sydney.', 7, 6, 12, 15, 'active', '2025-08-01', '2025-12-31', 1, 12, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00'),
(36, 'Canada Rockies Expedition', 'International', 112000.00, 'Discover the breathtaking Canadian Rockies.', 7, 6, 12, 12, 'active', '2025-08-01', '2025-12-31', 1, 10, 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `Gender` enum('Male','Female','Other','Prefer not to say') DEFAULT NULL,
  `Role` enum('Admin','User') NOT NULL DEFAULT 'User',
  `IsActive` tinyint(1) NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Email`, `Password`, `FirstName`, `LastName`, `Phone`, `Address`, `BirthDate`, `Gender`, `Role`, `IsActive`, `CreatedAt`, `UpdatedAt`) VALUES
(1, 'admin_ken', 'adminken@email.com', 'lphttken', 'Ken', 'Harold', NULL, NULL, NULL, NULL, 'Admin', 1, '2025-08-24 07:11:00', '2025-08-24 07:11:00');

-- --------------------------------------------------------

--
-- Structure for view `bookingamounts`
--
DROP TABLE IF EXISTS `bookingamounts`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bookingamounts`  AS SELECT `b`.`BookingID` AS `BookingID`, `b`.`BookingReference` AS `BookingReference`, `b`.`UserID` AS `UserID`, `b`.`PackageID` AS `PackageID`, `b`.`NumberOfPeople` AS `NumberOfPeople`, `b`.`PromoID` AS `PromoID`, (`tp`.`Price` * `b`.`NumberOfPeople`) AS `BaseAmount`, coalesce(`addon_totals`.`AddOnTotal`,0) AS `AddOnTotal`, ((`tp`.`Price` * `b`.`NumberOfPeople`) + coalesce(`addon_totals`.`AddOnTotal`,0)) AS `SubTotal`, (case when ((`b`.`PromoID` is not null) and (`pd`.`Status` = 'Approved')) then round((((`tp`.`Price` * `b`.`NumberOfPeople`) + coalesce(`addon_totals`.`AddOnTotal`,0)) * (`pt`.`DiscountPercentage` / 100)),2) else 0 end) AS `DiscountAmount`, (((`tp`.`Price` * `b`.`NumberOfPeople`) + coalesce(`addon_totals`.`AddOnTotal`,0)) - (case when ((`b`.`PromoID` is not null) and (`pd`.`Status` = 'Approved')) then round((((`tp`.`Price` * `b`.`NumberOfPeople`) + coalesce(`addon_totals`.`AddOnTotal`,0)) * (`pt`.`DiscountPercentage` / 100)),2) else 0 end)) AS `FinalAmount`, `pt`.`PromoTypeName` AS `PromoTypeName`, `pt`.`DiscountPercentage` AS `DiscountPercentage` FROM ((((`bookings` `b` join `tourpackages` `tp` on((`b`.`PackageID` = `tp`.`PackageID`))) left join `promodiscounts` `pd` on((`b`.`PromoID` = `pd`.`PromoID`))) left join `promotypes` `pt` on((`pd`.`PromoTypeID` = `pt`.`PromoTypeID`))) left join (select `bookingaddons`.`BookingID` AS `BookingID`,sum((`bookingaddons`.`UnitPrice` * `bookingaddons`.`Quantity`)) AS `AddOnTotal` from `bookingaddons` group by `bookingaddons`.`BookingID`) `addon_totals` on((`b`.`BookingID` = `addon_totals`.`BookingID`))) ;

-- --------------------------------------------------------

--
-- Structure for view `bookingcompleteview`
--
DROP TABLE IF EXISTS `bookingcompleteview`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bookingcompleteview`  AS SELECT `b`.`BookingID` AS `BookingID`, `b`.`BookingReference` AS `BookingReference`, `b`.`UserID` AS `UserID`, `u`.`FirstName` AS `FirstName`, `u`.`LastName` AS `LastName`, `u`.`Email` AS `Email`, `u`.`Phone` AS `Phone`, `b`.`BookingDate` AS `BookingDate`, `b`.`TravelDate` AS `TravelDate`, `b`.`EndDate` AS `EndDate`, `b`.`NumberOfPeople` AS `NumberOfPeople`, `b`.`Status` AS `Status`, `bp`.`PaymentMethod` AS `PaymentMethod`, `bp`.`PaymentStatus` AS `PaymentStatus`, `bp`.`PaymentDate` AS `PaymentDate`, `bp`.`TransactionReference` AS `TransactionReference`, `ba`.`BaseAmount` AS `BaseAmount`, `ba`.`AddOnTotal` AS `AddOnTotal`, `ba`.`SubTotal` AS `SubTotal`, `ba`.`DiscountAmount` AS `DiscountAmount`, `ba`.`FinalAmount` AS `FinalAmount`, `ba`.`PromoTypeName` AS `PromoTypeName`, `ba`.`DiscountPercentage` AS `DiscountPercentage`, `tp`.`PackageID` AS `PackageID`, `tp`.`Title` AS `PackageTitle`, `pl`.`Location` AS `PackageLocation`, `tp`.`PackageType` AS `PackageType` FROM (((((`bookings` `b` join `users` `u` on((`b`.`UserID` = `u`.`UserID`))) join `tourpackages` `tp` on((`b`.`PackageID` = `tp`.`PackageID`))) join `packagelocations` `pl` on((`tp`.`PackageID` = `pl`.`PackageID`))) left join `bookingpayments` `bp` on((`b`.`BookingID` = `bp`.`BookingID`))) left join `bookingamounts` `ba` on((`b`.`BookingID` = `ba`.`BookingID`))) ;

-- --------------------------------------------------------

--
-- Structure for view `bookingwithreviewsview`
--
DROP TABLE IF EXISTS `bookingwithreviewsview`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bookingwithreviewsview`  AS SELECT `b`.`BookingID` AS `BookingID`, `b`.`BookingReference` AS `BookingReference`, `b`.`UserID` AS `UserID`, concat(`u`.`FirstName`,' ',`u`.`LastName`) AS `CustomerName`, `u`.`FirstName` AS `FirstName`, `u`.`LastName` AS `LastName`, `u`.`Email` AS `Email`, `u`.`Phone` AS `Phone`, `b`.`BookingDate` AS `BookingDate`, `b`.`TravelDate` AS `TravelDate`, `b`.`EndDate` AS `EndDate`, (to_days(`b`.`EndDate`) - to_days(`b`.`TravelDate`)) AS `TripDuration`, `b`.`NumberOfPeople` AS `NumberOfPeople`, `b`.`Status` AS `Status`, `ba`.`FinalAmount` AS `FinalAmount`, `ba`.`BaseAmount` AS `BaseAmount`, `ba`.`AddOnTotal` AS `AddOnTotal`, `ba`.`DiscountAmount` AS `DiscountAmount`, `tp`.`PackageID` AS `PackageID`, `tp`.`Title` AS `PackageTitle`, `tp`.`PackageType` AS `PackageType`, `pl`.`Location` AS `PackageLocation`, `bp`.`PaymentMethod` AS `PaymentMethod`, `bp`.`PaymentStatus` AS `PaymentStatus`, `bp`.`PaymentDate` AS `PaymentDate`, `bp`.`TransactionReference` AS `TransactionReference`, `r`.`Rating` AS `Rating` FROM ((((((`bookings` `b` join `users` `u` on((`b`.`UserID` = `u`.`UserID`))) join `tourpackages` `tp` on((`b`.`PackageID` = `tp`.`PackageID`))) join `packagelocations` `pl` on((`tp`.`PackageID` = `pl`.`PackageID`))) left join `bookingpayments` `bp` on((`b`.`BookingID` = `bp`.`BookingID`))) left join `bookingamounts` `ba` on((`b`.`BookingID` = `ba`.`BookingID`))) left join `reviews` `r` on((`b`.`BookingID` = `r`.`BookingID`))) ;

-- --------------------------------------------------------

--
-- Structure for view `incomeamounts`
--
DROP TABLE IF EXISTS `incomeamounts`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `incomeamounts`  AS SELECT `income`.`IncomeID` AS `IncomeID`, `income`.`IncomeItem` AS `IncomeItem`, `income`.`IncomeType` AS `IncomeType`, `income`.`IncomeSourceID` AS `IncomeSourceID`, `income`.`BookingID` AS `BookingID`, `income`.`IncomeDate` AS `IncomeDate`, `income`.`Description` AS `Description`, `income`.`RecordedBy` AS `RecordedBy`, `income`.`RecordedAt` AS `RecordedAt` FROM `income` ;

-- --------------------------------------------------------

--
-- Structure for view `packageavailability`
--
DROP TABLE IF EXISTS `packageavailability`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `packageavailability`  AS SELECT `tp`.`PackageID` AS `PackageID`, `tp`.`Title` AS `Title`, `tp`.`PackageType` AS `PackageType`, `tp`.`MaxSlots` AS `MaxSlots`, coalesce(`booked_slots`.`BookedSlots`,0) AS `BookedSlots`, (`tp`.`MaxSlots` - coalesce(`booked_slots`.`BookedSlots`,0)) AS `AvailableSlots`, `tp`.`StartDate` AS `StartDate`, `tp`.`EndDate` AS `EndDate`, `tp`.`Status` AS `Status`, `tp`.`IsActive` AS `IsActive` FROM (`tourpackages` `tp` left join (select `bookings`.`PackageID` AS `PackageID`,sum(`bookings`.`NumberOfPeople`) AS `BookedSlots` from `bookings` where (`bookings`.`Status` in ('Pending','Confirmed')) group by `bookings`.`PackageID`) `booked_slots` on((`tp`.`PackageID` = `booked_slots`.`PackageID`))) ;

-- --------------------------------------------------------

--
-- Structure for view `recenttransactions`
--
DROP TABLE IF EXISTS `recenttransactions`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `recenttransactions`  AS SELECT 'Income' AS `Type`, `i`.`Description` AS `Description`, `ba`.`FinalAmount` AS `Amount`, `i`.`IncomeDate` AS `Date`, `bp`.`PaymentMethod` AS `PaymentMethod`, `i`.`RecordedBy` AS `UserID`, `i`.`BookingID` AS `BookingID`, `tp`.`PackageType` AS `PackageCategory`, `b`.`BookingDate` AS `BookingDate`, NULL AS `ExpenseItem`, NULL AS `ExpenseCategory`, NULL AS `ReceiptNumber`, NULL AS `AdminName`, 1 AS `IsIncome` FROM ((((`income` `i` left join `bookings` `b` on((`i`.`BookingID` = `b`.`BookingID`))) left join `bookingpayments` `bp` on((`i`.`BookingID` = `bp`.`BookingID`))) left join `tourpackages` `tp` on((`b`.`PackageID` = `tp`.`PackageID`))) left join `bookingamounts` `ba` on((`b`.`BookingID` = `ba`.`BookingID`)))union all select 'Expense' AS `Type`,`e`.`Description` AS `Description`,`e`.`Amount` AS `Amount`,`e`.`ExpenseDate` AS `Date`,`e`.`PaymentMethod` AS `PaymentMethod`,NULL AS `UserID`,`e`.`BookingID` AS `BookingID`,NULL AS `PackageCategory`,NULL AS `BookingDate`,`e`.`ExpenseItem` AS `ExpenseItem`,`ec`.`Category` AS `ExpenseCategory`,`e`.`ReceiptNumber` AS `ReceiptNumber`,concat(`u`.`FirstName`,' ',`u`.`LastName`) AS `AdminName`,0 AS `IsIncome` from ((`expenses` `e` left join `expensecategories` `ec` on((`e`.`ExpenseCategoryID` = `ec`.`ExpenseCategoryID`))) left join `users` `u` on((`e`.`RecordedBy` = `u`.`UserID`))) order by `Date` desc limit 20  ;

-- --------------------------------------------------------

--
-- Structure for view `reviewstatistics`
--
DROP TABLE IF EXISTS `reviewstatistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `reviewstatistics`  AS SELECT count(0) AS `TotalReviews`, round(avg(`reviews`.`Rating`),2) AS `AverageRating`, count((case when (`reviews`.`Rating` = 5) then 1 end)) AS `FiveStarCount`, count((case when (`reviews`.`Rating` = 4) then 1 end)) AS `FourStarCount`, count((case when (`reviews`.`Rating` = 3) then 1 end)) AS `ThreeStarCount`, count((case when (`reviews`.`Rating` = 2) then 1 end)) AS `TwoStarCount`, count((case when (`reviews`.`Rating` = 1) then 1 end)) AS `OneStarCount`, count((case when ((`reviews`.`Comment` is not null) and (`reviews`.`Comment` <> '')) then 1 end)) AS `ReviewsWithComments`, count((case when ((`reviews`.`Comment` is null) or (`reviews`.`Comment` = '')) then 1 end)) AS `ReviewsWithoutComments`, round(((count((case when (`reviews`.`Rating` = 5) then 1 end)) * 100.0) / count(0)),2) AS `FiveStarPercentage`, round(((count((case when (`reviews`.`Rating` = 4) then 1 end)) * 100.0) / count(0)),2) AS `FourStarPercentage`, round(((count((case when (`reviews`.`Rating` = 3) then 1 end)) * 100.0) / count(0)),2) AS `ThreeStarPercentage`, round(((count((case when (`reviews`.`Rating` = 2) then 1 end)) * 100.0) / count(0)),2) AS `TwoStarPercentage`, round(((count((case when (`reviews`.`Rating` = 1) then 1 end)) * 100.0) / count(0)),2) AS `OneStarPercentage` FROM `reviews` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookingaddons`
--
ALTER TABLE `bookingaddons`
  ADD PRIMARY KEY (`BookingAddOnID`),
  ADD KEY `idx_booking_id` (`BookingID`),
  ADD KEY `idx_addon_id` (`AddOnID`);

--
-- Indexes for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  ADD PRIMARY KEY (`HistoryID`),
  ADD KEY `BookingID` (`BookingID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `ModifiedBy` (`ModifiedBy`);

--
-- Indexes for table `bookingpackages`
--
ALTER TABLE `bookingpackages`
  ADD PRIMARY KEY (`BookingPackageID`),
  ADD KEY `BookingID` (`BookingID`),
  ADD KEY `PackageID` (`PackageID`);

--
-- Indexes for table `bookingpayments`
--
ALTER TABLE `bookingpayments`
  ADD PRIMARY KEY (`BookingID`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`BookingID`),
  ADD UNIQUE KEY `BookingReference` (`BookingReference`),
  ADD KEY `PromoID` (`PromoID`),
  ADD KEY `idx_user_id` (`UserID`),
  ADD KEY `idx_package_id` (`PackageID`),
  ADD KEY `idx_travel_date` (`TravelDate`),
  ADD KEY `idx_status` (`Status`);

--
-- Indexes for table `expensecategories`
--
ALTER TABLE `expensecategories`
  ADD PRIMARY KEY (`ExpenseCategoryID`),
  ADD UNIQUE KEY `Category` (`Category`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`ExpenseID`),
  ADD KEY `ExpenseCategoryID` (`ExpenseCategoryID`),
  ADD KEY `BookingID` (`BookingID`),
  ADD KEY `RecordedBy` (`RecordedBy`);

--
-- Indexes for table `income`
--
ALTER TABLE `income`
  ADD PRIMARY KEY (`IncomeID`),
  ADD KEY `BookingID` (`BookingID`),
  ADD KEY `IncomeSourceID` (`IncomeSourceID`),
  ADD KEY `RecordedBy` (`RecordedBy`);

--
-- Indexes for table `incomesources`
--
ALTER TABLE `incomesources`
  ADD PRIMARY KEY (`IncomeSourceID`);

--
-- Indexes for table `packageaddons`
--
ALTER TABLE `packageaddons`
  ADD PRIMARY KEY (`AddOnID`),
  ADD KEY `PackageID` (`PackageID`);

--
-- Indexes for table `packagedetails`
--
ALTER TABLE `packagedetails`
  ADD PRIMARY KEY (`PackageID`);

--
-- Indexes for table `packagelocations`
--
ALTER TABLE `packagelocations`
  ADD PRIMARY KEY (`PackageID`);

--
-- Indexes for table `promodiscounts`
--
ALTER TABLE `promodiscounts`
  ADD PRIMARY KEY (`PromoID`),
  ADD UNIQUE KEY `unique_user_promo` (`UserID`,`PromoTypeID`),
  ADD KEY `ValidatedBy` (`ValidatedBy`),
  ADD KEY `idx_user_id` (`UserID`),
  ADD KEY `idx_promo_type` (`PromoTypeID`),
  ADD KEY `idx_status` (`Status`);

--
-- Indexes for table `promotypes`
--
ALTER TABLE `promotypes`
  ADD PRIMARY KEY (`PromoTypeID`),
  ADD UNIQUE KEY `PromoTypeName` (`PromoTypeName`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`ReviewID`),
  ADD KEY `PackageID` (`PackageID`),
  ADD KEY `idx_user_id` (`UserID`),
  ADD KEY `idx_booking_id` (`BookingID`),
  ADD KEY `idx_rating` (`Rating`),
  ADD KEY `idx_review_date` (`ReviewDate`);

--
-- Indexes for table `tourcategories`
--
ALTER TABLE `tourcategories`
  ADD PRIMARY KEY (`CategoryID`),
  ADD UNIQUE KEY `CategoryName` (`CategoryName`);

--
-- Indexes for table `tourpackages`
--
ALTER TABLE `tourpackages`
  ADD PRIMARY KEY (`PackageID`),
  ADD KEY `CategoryID` (`CategoryID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookingaddons`
--
ALTER TABLE `bookingaddons`
  MODIFY `BookingAddOnID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  MODIFY `HistoryID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookingpackages`
--
ALTER TABLE `bookingpackages`
  MODIFY `BookingPackageID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `BookingID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `expensecategories`
--
ALTER TABLE `expensecategories`
  MODIFY `ExpenseCategoryID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `ExpenseID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `income`
--
ALTER TABLE `income`
  MODIFY `IncomeID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `incomesources`
--
ALTER TABLE `incomesources`
  MODIFY `IncomeSourceID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `packageaddons`
--
ALTER TABLE `packageaddons`
  MODIFY `AddOnID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `promodiscounts`
--
ALTER TABLE `promodiscounts`
  MODIFY `PromoID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `promotypes`
--
ALTER TABLE `promotypes`
  MODIFY `PromoTypeID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `ReviewID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tourcategories`
--
ALTER TABLE `tourcategories`
  MODIFY `CategoryID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `tourpackages`
--
ALTER TABLE `tourpackages`
  MODIFY `PackageID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookingaddons`
--
ALTER TABLE `bookingaddons`
  ADD CONSTRAINT `bookingaddons_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookingaddons_ibfk_2` FOREIGN KEY (`AddOnID`) REFERENCES `packageaddons` (`AddOnID`) ON DELETE CASCADE;

--
-- Constraints for table `bookinghistory`
--
ALTER TABLE `bookinghistory`
  ADD CONSTRAINT `bookinghistory_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookinghistory_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookinghistory_ibfk_3` FOREIGN KEY (`ModifiedBy`) REFERENCES `users` (`UserID`) ON DELETE SET NULL;

--
-- Constraints for table `bookingpackages`
--
ALTER TABLE `bookingpackages`
  ADD CONSTRAINT `bookingpackages_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`),
  ADD CONSTRAINT `bookingpackages_ibfk_2` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`);

--
-- Constraints for table `bookingpayments`
--
ALTER TABLE `bookingpayments`
  ADD CONSTRAINT `bookingpayments_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE CASCADE;

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`PromoID`) REFERENCES `promodiscounts` (`PromoID`) ON DELETE SET NULL;

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`ExpenseCategoryID`) REFERENCES `expensecategories` (`ExpenseCategoryID`) ON DELETE CASCADE,
  ADD CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE SET NULL,
  ADD CONSTRAINT `expenses_ibfk_3` FOREIGN KEY (`RecordedBy`) REFERENCES `users` (`UserID`) ON DELETE SET NULL;

--
-- Constraints for table `income`
--
ALTER TABLE `income`
  ADD CONSTRAINT `income_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE SET NULL,
  ADD CONSTRAINT `income_ibfk_2` FOREIGN KEY (`IncomeSourceID`) REFERENCES `incomesources` (`IncomeSourceID`) ON DELETE CASCADE,
  ADD CONSTRAINT `income_ibfk_3` FOREIGN KEY (`RecordedBy`) REFERENCES `users` (`UserID`) ON DELETE SET NULL;

--
-- Constraints for table `packageaddons`
--
ALTER TABLE `packageaddons`
  ADD CONSTRAINT `packageaddons_ibfk_1` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`) ON DELETE CASCADE;

--
-- Constraints for table `packagedetails`
--
ALTER TABLE `packagedetails`
  ADD CONSTRAINT `packagedetails_ibfk_1` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`) ON DELETE CASCADE;

--
-- Constraints for table `packagelocations`
--
ALTER TABLE `packagelocations`
  ADD CONSTRAINT `packagelocations_ibfk_1` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`) ON DELETE CASCADE;

--
-- Constraints for table `promodiscounts`
--
ALTER TABLE `promodiscounts`
  ADD CONSTRAINT `promodiscounts_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  ADD CONSTRAINT `promodiscounts_ibfk_2` FOREIGN KEY (`PromoTypeID`) REFERENCES `promotypes` (`PromoTypeID`) ON DELETE CASCADE,
  ADD CONSTRAINT `promodiscounts_ibfk_3` FOREIGN KEY (`ValidatedBy`) REFERENCES `users` (`UserID`) ON DELETE SET NULL;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`BookingID`) REFERENCES `bookings` (`BookingID`) ON DELETE SET NULL,
  ADD CONSTRAINT `reviews_ibfk_3` FOREIGN KEY (`PackageID`) REFERENCES `tourpackages` (`PackageID`) ON DELETE SET NULL;

--
-- Constraints for table `tourpackages`
--
ALTER TABLE `tourpackages`
  ADD CONSTRAINT `tourpackages_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `tourcategories` (`CategoryID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
